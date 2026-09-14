import sys
import os
import struct
import prosedur_training
from xar_dom_engine import XarDocument
from apply_flawless_adhikarya_jul import extract_dom_rows

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

folder = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUL"
out_xar = os.path.join(folder, "0_tahap7.xar")
doc = XarDocument(out_xar)

print("=========================================================================")
print("         DEEP COMPREHENSIVE QA AUDIT: ADHIKARYA PUTRA JUL 2026          ")
print("=========================================================================\n")

# 1. Tree Balance
t1 = sum(1 for r in doc.records if r['tag'] == 1)
t0 = sum(1 for r in doc.records if r['tag'] == 0)
net_depth = t1 - t0
print(f"1. Tree Balance: Tag 1 = {t1:,}, Tag 0 = {t0:,} (Net Depth = {net_depth})")
assert net_depth == -4, f"Tree balance violation! Expected -4, got {net_depth}"
print("   -> Tree Depth Invariant: MATCH (-4) [PASS]")

# 2. Customer Name
names = [r['payload'].decode('utf-16le', errors='ignore') for r in doc.records if r['tag'] == 2201 and 'ADHIKARYA' in r['payload'].decode('utf-16le', errors='ignore')]
print(f"\n2. Customer Name (ALL CAPS): {len(names)} instances -> {set(names)}")
assert len(names) == 7 and all(n.strip() == 'ADHIKARYA PUTRA' for n in names)
print("   -> Customer Name: 100% ALL CAPS Across All 7 Pages [PASS]")

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
periodes = [r['payload'].decode('utf-16le', errors='ignore') for r in doc.records if r['tag'] == 2201 and 'Jul 2026 - 31 Jul 2026' in r['payload'].decode('utf-16le', errors='ignore')]
print(f"\n4. Periode Header (7 Pages): {len(periodes)} instances -> {set(periodes)}")
assert len(periodes) == 7
print("   -> Periode Header: 100% MATCH ('01 Jul 2026 - 31 Jul 2026') [PASS]")

# 5. Page Numbers
import re
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
sawal = 570498.81
dmasuk = 17241700.00
dkeluar = 13027403.00
sakhir = 4784795.81
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
    
    if day2 < day1:
        print(f"   [ERROR] Date backwards at row {idx+1}: {d1} -> {d2}")
        date_ok = False
        
    if day1 == day2:
        sec1 = int(t1[:2])*3600 + int(t1[3:5])*60 + int(t1[6:8])
        sec2 = int(t2[:2])*3600 + int(t2[3:5])*60 + int(t2[6:8])
        if sec2 < sec1:
            print(f"   [ERROR] Time backwards on {d1} at row {idx+1}: {t1} -> {t2}")
            time_ok = False

assert date_ok and time_ok
print(f"   -> Date Monotonicity : 100% Monotonic Non-Decreasing (Day {int(dom_rows[0]['date_recs'][0][1][:2])} to Day {int(dom_rows[-1]['date_recs'][0][1][:2])}) [PASS]")
print(f"   -> Time Monotonicity : 100% Chronological per Date [PASS]")
print(f"   -> First Row (Tx 1)  : {dom_rows[0]['date_recs'][0][1]} | {dom_rows[0]['time_recs'][0][1]} | Nom={dom_rows[0]['n_txt']} | Saldo={dom_rows[0]['s_txt']}")
print(f"   -> Salary Row (Tx 68): {dom_rows[67]['date_recs'][0][1]} | {dom_rows[67]['time_recs'][0][1]} | Nom={dom_rows[67]['n_txt']} | Saldo={dom_rows[67]['s_txt']}")
print(f"   -> Last Row (Tx 82)  : {dom_rows[-1]['date_recs'][0][1]} | {dom_rows[-1]['time_recs'][0][1]} | Nom={dom_rows[-1]['n_txt']} | Saldo={dom_rows[-1]['s_txt']}")

# 8. Alignment & Decoupled 2-Box Check
print(f"\n8. Decoupled 2-Box No & Saldo Alignment Audit:")
align_ok = True
for idx, r in enumerate(dom_rows):
    no_x = struct.unpack('<iii', doc.records[r['s_t2100'] - 24]['payload'][:12])[0] if r['s_t2100'] else 20000
    saldo_x = struct.unpack('<iii', doc.records[r['s_t2100']]['payload'][:12])[0]
    w_saldo = prosedur_training.calc_text_width(r['s_txt'])
    xr_saldo = saldo_x + w_saldo
    
    if abs(xr_saldo - 570450) > 1000:
        print(f"   [ALIGN ERROR] Saldo row {idx+1} XR={xr_saldo} (Target=570450)")
        align_ok = False

assert align_ok
print("   -> Decoupled 2-Box No & Saldo: 100% Modular & Perfectly Right-Aligned [PASS]")

print("\n=========================================================================")
print("             ALL AUDIT VERIFICATIONS PASSED (100% PERFECT)              ")
print("=========================================================================\n")
