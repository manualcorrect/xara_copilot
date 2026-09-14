import json
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

with open('aug_rows_map.json') as f:
    rows = json.load(f)

print("=== ORIGINAL DATES IN AUG/0.XAR (110 ROWS) ===")
for r in rows:
    d_prim = r.get('date_prim')
    d_sec = r.get('date_sec')
    t_prim = r.get('time_prim')
    t_sec = r.get('time_sec')
    d_txt = doc.records[d_prim]['payload'].decode('utf-16le', errors='ignore') if d_prim else None
    t_txt = doc.records[t_prim]['payload'].decode('utf-16le', errors='ignore') if t_prim else None
    print(f"Row {r['row_idx']:3d} | Date: {d_txt!r:20s} | Time: {t_txt!r:20s}")
