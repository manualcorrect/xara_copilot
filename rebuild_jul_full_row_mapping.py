import json
import struct
from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

with open('jul_final_tx_schedule.json', 'r', encoding='utf-8') as f:
    txs = json.load(f)

print("=" * 80)
print("COMPREHENSIVE ROW AUDIT & SECONDARY SPLIT MAPPING (JULY 83 ROWS)")
print("=" * 80)

# Build a precise list of 83 row records
detailed_rows = []

# Scan through doc to find each row number and its associated elements
for i in range(len(doc.records)):
    r = doc.records[i]
    if r['tag'] == 2204 and i + 6 < len(doc.records):
        for k in range(i+1, min(len(doc.records), i+10)):
            rk = doc.records[k]
            if rk['tag'] in (2201, 2202):
                txt = rk['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if ',' in txt and (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0'):
                    # Row number is before Tag 2204
                    row_no_rec = None
                    row_no_val = None
                    for p in range(max(0, i-6), i):
                        if doc.records[p]['tag'] in (2201, 2202):
                            r_txt = doc.records[p]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                            if r_txt.isdigit():
                                row_no_rec = p
                                row_no_val = int(r_txt)
                                break
                    if row_no_rec:
                        # Find nominal after saldo (primary and secondary split nodes)
                        nom_primary = None
                        nom_secondary = None
                        nom_tag2206 = None
                        nom_tag2100 = None
                        nom_tag150 = None
                        
                        for n in range(k+1, min(len(doc.records), k+45)):
                            rn = doc.records[n]
                            if rn['tag'] in (2201, 2202):
                                n_txt = rn['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                if (n_txt.startswith('-') or n_txt.startswith('+')) and ',' in n_txt:
                                    nom_primary = n
                                    # Check if followed by secondary split
                                    for s in range(n+1, min(len(doc.records), n+10)):
                                        rs = doc.records[s]
                                        if rs['tag'] in (2201, 2202):
                                            s_txt = rs['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                            if s_txt and (s_txt.endswith(',00') or s_txt.isdigit() or ',' in s_txt):
                                                nom_secondary = s
                                                break
                                    break
                                elif n_txt.startswith('-') or n_txt.startswith('+'):
                                    nom_primary = n
                                    # Secondary split holds the decimals/ending
                                    for s in range(n+1, min(len(doc.records), n+10)):
                                        rs = doc.records[s]
                                        if rs['tag'] in (2201, 2202):
                                            s_txt = rs['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                            if s_txt:
                                                nom_secondary = s
                                                break
                                    break
                                    
                        # Find Tag 2206, Tag 2100, Tag 150 before nom_primary
                        if nom_primary:
                            for t6 in range(max(0, nom_primary-6), nom_primary):
                                if doc.records[t6]['tag'] == 2206:
                                    nom_tag2206 = t6
                                    break
                            for t1 in range(max(0, nom_primary-30), nom_primary):
                                if doc.records[t1]['tag'] == 2100:
                                    nom_tag2100 = t1
                                    break
                            for c in range(max(0, nom_primary-20), nom_primary):
                                if doc.records[c]['tag'] == 150:
                                    nom_tag150 = c
                                    break
                                    
                        # Find Date and Time before row number
                        date_rec = None
                        time_rec = None
                        for d in range(max(0, row_no_rec-35), row_no_rec):
                            rd = doc.records[d]
                            if rd['tag'] in (2201, 2202):
                                d_txt = rd['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                if 'Feb 2026' in d_txt and len(d_txt) >= 10:
                                    date_rec = d
                                elif 'WIB' in d_txt or (':' in d_txt and any(c.isdigit() for c in d_txt)):
                                    time_rec = d
                                    
                        dx, dy = struct.unpack('<ii', doc.records[i]['payload'][:8])
                        detailed_rows.append({
                            "row_num": row_no_val,
                            "row_no_rec": row_no_rec,
                            "tag2204_rec": i,
                            "orig_dx": dx,
                            "orig_dy": dy,
                            "saldo_rec": k,
                            "orig_saldo": txt,
                            "nom_primary": nom_primary,
                            "nom_secondary": nom_secondary,
                            "nom_tag2206": nom_tag2206,
                            "nom_tag2100": nom_tag2100,
                            "nom_tag150": nom_tag150,
                            "date_rec": date_rec,
                            "time_rec": time_rec
                        })
                    break

print(f"Total detailed rows mapped: {len(detailed_rows)}")
assert len(detailed_rows) == 83, f"Expected 83 rows, got {len(detailed_rows)}"

for r in detailed_rows[:10]:
    print(f"Row {r['row_num']:2d} | Saldo Rec {r['saldo_rec']:5d} (Tag 2204 Rec {r['tag2204_rec']:5d}) | Nom Prim: {r['nom_primary']}, Sec: {r['nom_secondary']} | Date: {r['date_rec']}, Time: {r['time_rec']}")

with open('jul_detailed_rows.json', 'w', encoding='utf-8') as f:
    json.dump(detailed_rows, f, indent=2)

print("[OK] Detailed rows saved to jul_detailed_rows.json")
