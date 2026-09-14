import os
import struct
import json
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
p0 = os.path.join(folder, '0.xar')
doc = XarDocument(p0)

print("=== MAPPING ALL 73 ROWS IN JUN 0.XAR ===")
rows_map = []
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
                orig_dx, orig_dy = struct.unpack('<ii', doc.records[i]['payload'][:8])
                orig_saldo = doc.records[saldo_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                
                nom_prim, nom_sec, nom_t150, nom_t2100, nom_t2206 = None, None, None, None, None
                for n in range(saldo_rec+1, min(len(doc.records), saldo_rec+45)):
                    rn = doc.records[n]
                    if rn['tag'] in (2201, 2202):
                        ntxt = rn['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                        if ntxt.startswith('+') or ntxt.startswith('-'):
                            nom_prim = n
                            for s in range(n+1, min(len(doc.records), n+8)):
                                if doc.records[s]['tag'] in (2201, 2202):
                                    stxt = doc.records[s]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                    if stxt and (stxt.endswith(',00') or stxt.isdigit() or ',' in stxt):
                                        nom_sec = s
                                        break
                            break
                if nom_prim:
                    for c in range(max(0, nom_prim-25), nom_prim):
                        if doc.records[c]['tag'] == 150:
                            nom_t150 = c
                    for t1 in range(max(0, nom_prim-30), nom_prim):
                        if doc.records[t1]['tag'] == 2100:
                            nom_t2100 = t1
                    for t6 in range(max(0, nom_prim-6), nom_prim):
                        if doc.records[t6]['tag'] == 2206:
                            nom_t2206 = t6
                            
                time_prim, time_sec, date_prim, date_sec = None, None, None, None
                search_start = (nom_sec or nom_prim or saldo_rec) + 1
                for tm in range(search_start, min(len(doc.records), search_start+60)):
                    rtm = doc.records[tm]
                    if rtm['tag'] in (2201, 2202):
                        ttxt = rtm['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                        if ('WIB' in ttxt or ':' in ttxt) and not time_prim:
                            time_prim = tm
                            for ts in range(tm+1, min(len(doc.records), tm+6)):
                                if doc.records[ts]['tag'] in (2201, 2202):
                                    tstxt = doc.records[ts]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                    if 'WIB' in tstxt or 'WI' in tstxt or 'B' in tstxt or tstxt.isdigit():
                                        time_sec = ts
                                        break
                        elif any(m in ttxt for m in ['Feb 2026', 'Jul 2026', 'Jan 2026', 'Jun 2026', 'Mar 2026']) and not date_prim:
                            date_prim = tm
                            for ds in range(max(0, tm-6), tm):
                                if doc.records[ds]['tag'] in (2201, 2202):
                                    dstxt = doc.records[ds]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                    if dstxt.isdigit():
                                        date_sec = ds
                                        break
                rows_map.append({
                    'row_idx': len(rows_map) + 1,
                    'row_no_val': row_no_val,
                    'row_no_rec': row_no_rec,
                    'saldo_rec': saldo_rec,
                    'orig_saldo': orig_saldo,
                    'tag2204_rec': i,
                    'orig_dx': orig_dx,
                    'orig_dy': orig_dy,
                    'nom_prim': nom_prim,
                    'nom_sec': nom_sec,
                    'nom_t150': nom_t150,
                    'nom_t2100': nom_t2100,
                    'nom_t2206': nom_t2206,
                    'time_prim': time_prim,
                    'time_sec': time_sec,
                    'date_prim': date_prim,
                    'date_sec': date_sec
                })

print(f"Total rows mapped: {len(rows_map)}")
with open('jun_rows_map.json', 'w', encoding='utf-8') as f:
    json.dump(rows_map, f, indent=2)
