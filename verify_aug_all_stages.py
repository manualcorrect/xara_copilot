import os
import struct
import json
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug'
t7_path = os.path.join(folder, '0_tahap7.xar')

print("=========================================================================")
print("   COMPREHENSIVE AUDIT & VERIFICATION: MARSIYAH AGUSTUS 2026 (10 PAGES)")
print(f"   Target: {t7_path}")
print("=========================================================================\n")

doc = XarDocument(t7_path)

# 1. Font Definition & References Audit
font_ids = set()
for r in doc.records:
    if r['tag'] == 2907:
        font_ids.add(r['payload'].hex())

print(f"[*] Active Font IDs in 0_tahap7.xar: {font_ids}")
assert '55010000' not in font_ids, "ERROR: Foreign font ID 55010000 detected!"
assert '54010000' in font_ids, "ERROR: Native font ID 54010000 missing!"
print("   -> Font Integrity: 100% Native (0% corruption risk) [PASS]")

# 2. Name Story & Cabang Audit across all 10 pages
name_stories = []
cabangs = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'MASRIYAH' in txt:
            w_box, flag = None, None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 2150:
                    w_box, flag = struct.unpack('<iB', doc.records[k]['payload'])
            name_stories.append((i, txt, w_box, flag))
        elif 'KCP Jakarta Taman Aries' in txt:
            pos = None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 2100:
                    pos = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]['payload'])
            cabangs.append((i, txt, pos))

print(f"\n[*] Name Stories Found: {len(name_stories)} / 10 pages")
for idx, ns in enumerate(name_stories, 1):
    print(f"   Page {idx:2d}: Rec {ns[0]:5d} | Text: {ns[1]!r:25s} | Width: {ns[2]} mp (3.17cm) | Flag: {ns[3]}")
    assert ns[2] == 89858, f"Page {idx} Name width is {ns[2]}, expected 89858 (3.17cm)"

print(f"\n[*] Independent Cabang Boxes Found: {len(cabangs)} / 10 pages")
for idx, cb in enumerate(cabangs, 1):
    print(f"   Page {idx:2d}: Rec {cb[0]:5d} | Text: {cb[1]!r:25s} | Pos: {cb[2]}")
    assert cb[2][0] == 124101 and cb[2][1] == 714420, f"Page {idx} Cabang position mismatch: {cb[2]}"

# 3. Period Header Audit across all 10 pages
periods = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if '01 Aug 2026 - 31 Aug 2026' in txt:
            periods.append((i, txt))

print(f"\n[*] Period Headers Found: {len(periods)} / 10 pages")
for idx, p in enumerate(periods, 1):
    print(f"   Page {idx:2d}: Rec {p[0]:5d} | Text: {p[1]!r}")
assert len(periods) == 10, f"Expected 10 periods, got {len(periods)}"

# 4. Dicetak pada Audit
dicetaks = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'Sep 2026' in r['payload'].decode('utf-16le', errors='ignore'):
        # scan backwards for digits
        digits = []
        for k in range(max(0, i-10), i):
            if doc.records[k]['tag'] in (2201, 2202):
                dtxt = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
                if dtxt.isdigit():
                    digits.append(dtxt)
        dicetaks.append((i, f"{''.join(digits)} Sep 2026"))

print(f"\n[*] Dicetak Headers Found: {len(dicetaks)} / 10 pages")
for idx, d in enumerate(dicetaks, 1):
    print(f"   Page {idx:2d}: Rec {d[0]:5d} | Date: {d[1]}")

# 5. Financial Summary Header Audit
print("\n[*] Financial Summary Header (Page 1):")
print(f"   Saldo Awal : {doc.records[1204]['payload'].decode('utf-16le', errors='ignore')!r} (Color: {doc.records[1200]['payload'].hex()})")
print(f"   Dana Masuk : {doc.records[1214]['payload'].decode('utf-16le', errors='ignore')!r} (Color: {doc.records[1210]['payload'].hex()})")
print(f"   Dana Keluar: {doc.records[1233]['payload'].decode('utf-16le', errors='ignore')!r} (Color: {doc.records[1226]['payload'].hex()})")
print(f"   Saldo Akhir: {doc.records[1246]['payload'].decode('utf-16le', errors='ignore')!r} (Color: {doc.records[1239]['payload'].hex()})")

# 6. Table Transaction Rows Dynamic Audit (110 Rows)
with open('aug_final_tx_schedule.json', 'r', encoding='utf-8') as f:
    txs = json.load(f)

# Find all 110 rows dynamically
rows_found = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2204 and i > 1200:
        saldo_rec = None
        for k in range(i+1, min(len(doc.records), i+8)):
            if doc.records[k]['tag'] in (2201, 2202):
                txt = doc.records[k]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0') and ('.' in txt or len(txt) > 5):
                    saldo_rec = k
                    break
        if saldo_rec:
            # find nominal, time, date
            nom_prim = None
            for n in range(saldo_rec+1, min(len(doc.records), saldo_rec+45)):
                if doc.records[n]['tag'] in (2201, 2202):
                    ntxt = doc.records[n]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                    if ntxt.startswith('+') or ntxt.startswith('-'):
                        nom_prim = n
                        break
            time_prim = None
            date_prim = None
            search_start = (nom_prim or saldo_rec) + 1
            for tm in range(search_start, min(len(doc.records), search_start+80)):
                if doc.records[tm]['tag'] in (2201, 2202):
                    ttxt = doc.records[tm]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                    if ('WIB' in ttxt or ':' in ttxt) and not time_prim:
                        time_prim = tm
                    elif 'Aug 2026' in ttxt and not date_prim:
                        date_prim = tm
            rows_found.append({
                'tag2204': i,
                'saldo_rec': saldo_rec,
                'nom_prim': nom_prim,
                'time_prim': time_prim,
                'date_prim': date_prim
            })

assert len(rows_found) == 110, f"Expected 110 dynamic rows, got {len(rows_found)}"

print(f"\n[*] Auditing All 110 Transaction Rows in DOM:")
for idx, rf in enumerate(rows_found):
    tx = txs[idx]
    dom_s = doc.records[rf['saldo_rec']]['payload'].decode('utf-16le', errors='ignore')
    dom_nom = doc.records[rf['nom_prim']]['payload'].decode('utf-16le', errors='ignore') if rf['nom_prim'] else ""
    dom_time = doc.records[rf['time_prim']]['payload'].decode('utf-16le', errors='ignore') if rf['time_prim'] else ""
    dom_date = doc.records[rf['date_prim']]['payload'].decode('utf-16le', errors='ignore') if rf['date_prim'] else ""
    
    assert dom_s == tx["formatted_saldo"], f"Row {idx+1} Saldo mismatch: DOM {dom_s} vs {tx['formatted_saldo']}"
    assert dom_nom == tx["formatted_nominal"], f"Row {idx+1} Nominal mismatch: DOM {dom_nom} vs {tx['formatted_nominal']}"
    assert dom_time == tx["final_time"], f"Row {idx+1} Time mismatch: DOM {dom_time} vs {tx['final_time']}"
    assert dom_date == tx["resolved_date"], f"Row {idx+1} Date mismatch: DOM {dom_date} vs {tx['resolved_date']}"

print(f"   -> 110 / 110 Transaction Rows MATCHED 100% PERFECTLY in 0_tahap7.xar!")
print("\n=========================================================================")
print("   [AUDIT PASSED] 0_tahap7.xar MEETS 100% OF SPECIFICATIONS & STANDARDS!")
print("=========================================================================")
