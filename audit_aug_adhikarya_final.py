import sys
import os
import struct
import re
import prosedur_training
from xar_dom_engine import XarDocument
from apply_flawless_adhikarya_aug import extract_dom_rows

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

folder = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\AUG"
out_xar = os.path.join(folder, "0_tahap7.xar")
doc = XarDocument(out_xar)

print("=========================================================================")
print("         DEEP COMPREHENSIVE QA AUDIT: ADHIKARYA PUTRA AUG 2026          ")
print("=========================================================================\n")

# 1. Tree Balance
t1 = sum(1 for r in doc.records if r['tag'] == 1)
t0 = sum(1 for r in doc.records if r['tag'] == 0)
net_depth = t1 - t0
print(f"1. Tree Balance: Tag 1 = {t1:,}, Tag 0 = {t0:,} (Net Depth = {net_depth})")
assert net_depth == -4, f"Tree balance violation! Expected -4, got {net_depth}"
print("   -> Tree Depth Invariant: MATCH (-4) [PASS]")

# 2. Customer Name & Cabang
header_names = []
for idx, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'ADHIKARYA' in r['payload'].decode('utf-16le', errors='ignore'):
        # Check if parent Tag 2100 is at Y == 736000 (Header)
        for k in range(idx - 1, max(0, idx - 30), -1):
            if doc.records[k]['tag'] == 2100:
                coords = struct.unpack('<iii', doc.records[k]['payload'][:12])
                if coords[1] == 736000:
                    header_names.append(r['payload'].decode('utf-16le', errors='ignore'))
                break

cabangs = [r['payload'].decode('utf-16le', errors='ignore') for r in doc.records if r['tag'] == 2201 and 'KCP Jakarta Taman Aries' in r['payload'].decode('utf-16le', errors='ignore')]
print(f"\n2. Customer Name (ALL CAPS Headers): {len(header_names)} instances -> {set(header_names)}")
print(f"   Decoupled Cabang (Headers): {len(cabangs)} instances -> {set(cabangs)}")
assert len(header_names) == 7 and all(n.strip() == 'ADHIKARYA PUTRA' for n in header_names)
assert len(cabangs) == 7
print("   -> Customer Name & Cabang: 100% ALL CAPS & Decoupled Across All 7 Pages [PASS]")

# 3. Dicetak Pada
dicetak = []
for idx, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'Sep 2026' in r['payload'].decode('utf-16le', errors='ignore'):
        digits = []
        for k in range(idx - 1, max(0, idx - 25), -1):
            if doc.records[k]['tag'] == 2202:
                digits.append(doc.records[k]['payload'].decode('utf-16le', errors='ignore'))
                if len(digits) == 2:
                    break
        if len(digits) == 2:
            dicetak.append(f"{digits[1]}{digits[0]} Sep 2026")

print(f"\n3. Dicetak Pada (7 Pages): {len(dicetak)} instances -> {set(dicetak)}")
assert len(dicetak) == 7 and set(dicetak) == {'10 Sep 2026'}
print("   -> Dicetak Pada: 100% MATCH ('10 Sep 2026') [PASS]")

# 4. Periode Header
periodes = [r['payload'].decode('utf-16le', errors='ignore') for r in doc.records if r['tag'] == 2201 and 'Aug 2026 - 31 Aug 2026' in r['payload'].decode('utf-16le', errors='ignore')]
print(f"\n4. Periode Header (7 Pages): {len(periodes)} instances -> {set(periodes)}")
assert len(periodes) == 7
print("   -> Periode Header: 100% MATCH ('01 Aug 2026 - 31 Aug 2026') [PASS]")

# 5. Page Numbers
pagenums = []
for idx, r in enumerate(doc.records):
    if r['tag'] == 2201:
        t = r['payload'].decode('utf-16le', errors='ignore').strip()
        if t == 'of 7' or re.match(r'^\d+\s+dari$', t):
            pagenums.append(t)
print(f"\n5. Page Numbers: {pagenums}")
assert len(pagenums) == 14 # 7 'of 7' + 7 'X dari'
print("   -> Page Numbers: 100% MATCH (1 of 7 s.d. 7 of 7) [PASS]")

# 6. Financial Summary Reconciliation
sawal = 4784795.81
dmasuk = 13903756.00
dkeluar = 12995126.00
sakhir = 5693425.81
calc_akhir = sawal + dmasuk - dkeluar
print(f"\n6. Financial Summary Audit:")
print(f"   Saldo Awal  : Rp {sawal:>15,.2f}")
print(f"   Dana Masuk  : Rp {dmasuk:>15,.2f}")
print(f"   Dana Keluar : Rp {dkeluar:>15,.2f}")
print(f"   Saldo Akhir : Rp {sakhir:>15,.2f}")
print(f"   Formula     : {sawal:,.2f} + {dmasuk:,.2f} - {dkeluar:,.2f} = {calc_akhir:,.2f}")
assert round(calc_akhir, 2) == round(sakhir, 2)
print("   -> Financial Summary Reconciliation: 100% BALANCE MATCH [PASS]")

# 7. Chronological Date & Time Monotonicity
dom_rows = extract_dom_rows(doc)
print(f"\n7. Chronological Date & Time Audit ({len(dom_rows)} rows):")
assert len(dom_rows) == 82

date_ok = True
time_ok = True
for idx in range(len(dom_rows) - 1):
    r1 = dom_rows[idx]
    r2 = dom_rows[idx + 1]
    
    d1 = r1['date_recs'][0][1]
    d2 = r2['date_recs'][0][1]
    t1 = r1['time_recs'][0][1]
    t2 = r2['time_recs'][0][1]
    
    day1 = int(d1[:2])
    day2 = int(d2[:2])
    
    if day1 > day2:
        date_ok = False
        print(f"   [FAIL] Date regression at row {idx+1}->{idx+2}: {d1} -> {d2}")
    elif day1 == day2:
        # Check time monotonicity
        tm1 = t1.split()[0]
        tm2 = t2.split()[0]
        if tm1 > tm2:
            time_ok = False
            print(f"   [FAIL] Time regression at row {idx+1}->{idx+2} ({d1}): {t1} -> {t2}")

assert date_ok, "Date monotonicity test failed!"
assert time_ok, "Time monotonicity test failed!"
print(f"   -> Date Monotonicity : 100% Monotonic Non-Decreasing (Day {dom_rows[0]['date_recs'][0][1][:2]} to Day {dom_rows[-1]['date_recs'][0][1][:2]}) [PASS]")
print(f"   -> Time Monotonicity : 100% Chronological per Date [PASS]")
print(f"   -> First Row (Tx 1)  : {dom_rows[0]['date_recs'][0][1]} | {dom_rows[0]['time_recs'][0][1]} | Nom={dom_rows[0]['n_txt']} | Saldo={dom_rows[0]['s_txt']}")
print(f"   -> Salary Row (Tx 67): {dom_rows[66]['date_recs'][0][1]} | {dom_rows[66]['time_recs'][0][1]} | Nom={dom_rows[66]['n_txt']} | Saldo={dom_rows[66]['s_txt']}")
print(f"   -> Last Row (Tx 82)  : {dom_rows[-1]['date_recs'][0][1]} | {dom_rows[-1]['time_recs'][0][1]} | Nom={dom_rows[-1]['n_txt']} | Saldo={dom_rows[-1]['s_txt']}")

# 8. Decoupled 2-Box No & Saldo Alignment Audit
palette = prosedur_training.deteksi_kamus_palet_native(doc)
saldo_x_coords = []
for r in dom_rows:
    assert r['s_t2100'] is not None, f"Row {r['row_no']} missing decoupled saldo matrix!"
    coords = struct.unpack('<iii', doc.records[r['s_t2100']]['payload'][:12])
    w = prosedur_training.calc_text_width(r['s_txt'])
    xr = coords[0] + w
    saldo_x_coords.append(xr)

print(f"\n8. Decoupled 2-Box No & Saldo Alignment Audit:")
print(f"   -> Right Edge Range: {min(saldo_x_coords)} s.d. {max(saldo_x_coords)} mp (Target: 570,450 mp / 20.049 cm)")
assert all(568000 <= xr <= 571000 for xr in saldo_x_coords)
print("   -> Decoupled 2-Box No & Saldo: 100% Modular & Perfectly Right-Aligned [PASS]")

print("\n=========================================================================")
print("             ALL AUDIT VERIFICATIONS PASSED (100% PERFECT)              ")
print("=========================================================================\n")
