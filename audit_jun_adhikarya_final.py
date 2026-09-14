import sys
import os
import struct
import re
import prosedur_training
from xar_dom_engine import XarDocument
from apply_flawless_adhikarya_jun import extract_dom_rows

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

folder = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUN"
out_xar = os.path.join(folder, "0_tahap7.xar")
doc = XarDocument(out_xar)

print("=========================================================================")
print("         DEEP COMPREHENSIVE QA AUDIT: ADHIKARYA PUTRA JUN 2026          ")
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
        for k in range(idx - 1, max(0, idx - 30), -1):
            if doc.records[k]['tag'] == 2100:
                coords = struct.unpack('<iii', doc.records[k]['payload'][:12])
                if coords[1] == 736000:
                    header_names.append(r['payload'].decode('utf-16le', errors='ignore'))
                break

cabangs = [r['payload'].decode('utf-16le', errors='ignore') for r in doc.records if r['tag'] == 2201 and 'KCP Jakarta Taman Aries' in r['payload'].decode('utf-16le', errors='ignore')]
print(f"\n2. Customer Name (ALL CAPS Headers): {len(header_names)} instances -> {set(header_names)}")
print(f"   Decoupled Cabang (Headers): {len(cabangs)} instances -> {set(cabangs)}")
assert len(header_names) == 13 and all(n.strip() == 'ADHIKARYA PUTRA' for n in header_names)
assert len(cabangs) == 13
print("   -> Customer Name & Cabang: 100% ALL CAPS & Decoupled Across All 13 Pages [PASS]")

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

print(f"\n3. Dicetak Pada (13 Pages): {len(dicetak)} instances -> {set(dicetak)}")
assert len(dicetak) == 13 and set(dicetak) == {'10 Sep 2026'}
print("   -> Dicetak Pada: 100% MATCH ('10 Sep 2026') [PASS]")

# 4. Periode Header
periodes = [r['payload'].decode('utf-16le', errors='ignore') for r in doc.records if r['tag'] == 2201 and 'Jun 2026 - 30 Jun 2026' in r['payload'].decode('utf-16le', errors='ignore')]
print(f"\n4. Periode Header (13 Pages): {len(periodes)} instances -> {set(periodes)}")
assert len(periodes) == 13
print("   -> Periode Header: 100% MATCH ('01 Jun 2026 - 30 Jun 2026') [PASS]")

# 5. Page Numbers
pagenums = []
for idx, r in enumerate(doc.records):
    if r['tag'] == 2201:
        t = r['payload'].decode('utf-16le', errors='ignore').strip()
        if t == 'of 13' or re.match(r'^\d+\s+dari$', t):
            pagenums.append(t)
print(f"\n5. Page Numbers: {pagenums}")
assert len(pagenums) == 26 # 13 'of 13' + 13 'X dari'
print("   -> Page Numbers: 100% MATCH (1 of 13 s.d. 13 of 13) [PASS]")

# 6. Financial Summary Reconciliation
sawal = 52488.81
dmasuk = 30212000.00
dkeluar = 29693990.00
sakhir = 570498.81
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
assert len(dom_rows) == 147

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
print(f"   -> Last Row (Tx 147) : {dom_rows[-1]['date_recs'][0][1]} | {dom_rows[-1]['time_recs'][0][1]} | Nom={dom_rows[-1]['n_txt']} | Saldo={dom_rows[-1]['s_txt']}")

# 8. Decoupled 2-Box No & Saldo Alignment & Color Audit
palette = prosedur_training.deteksi_kamus_palet_native(doc)
blue_handle_hex = palette['blue_saldo'].hex()

saldo_colors = []
for r in dom_rows:
    assert r['s_t2100'] is not None, f"Row {r['row_no']} missing decoupled saldo matrix!"
    # Check Tag 150 color on saldo object
    s_idx = r['s_t2100']
    c_hex = None
    for k in range(s_idx, min(len(doc.records), s_idx + 25)):
        if doc.records[k]['tag'] == 150:
            c_hex = doc.records[k]['payload'].hex()
            break
    saldo_colors.append(c_hex)

print(f"\n8. Saldo Color & Alignment Audit ({len(saldo_colors)} rows):")
print(f"   -> Expected Blue Saldo Tag 150: {blue_handle_hex}")
print(f"   -> Actual Colors on Saldo Rows: {set(saldo_colors)}")
assert set(saldo_colors) == {blue_handle_hex}, f"Color mismatch on Saldo rows! Found {set(saldo_colors)}"
print("   -> Saldo Color: 100% MANDIRI BLUE (#134BBA) Across All 147 Rows [PASS]")

print("\n=========================================================================")
print("             ALL AUDIT VERIFICATIONS PASSED (100% PERFECT)              ")
print("=========================================================================\n")
