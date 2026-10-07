import json
import struct
from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

def get_txt(idx):
    if 0 <= idx < len(doc.records):
        r = doc.records[idx]
        if r['tag'] in (2201, 2202, 2203):
            return r['payload'].decode('utf-16le', errors='ignore')
    return ""

def get_pos(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2100:
        return struct.unpack('<iii', doc.records[idx]['payload'][:12])
    return None

def get_kern(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2206:
        return struct.unpack('<iii', doc.records[idx]['payload'][:12])
    return None

def get_color(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 150:
        return doc.records[idx]['payload'].hex()
    return None

# Let's inspect the exact neighborhood for each of the 19 rows
row_ranges = [
    (1, 1500, 1680),
    (2, 1680, 1840),
    (3, 1840, 2010),
    (4, 2010, 2180),
    (5, 2180, 2350),
    (6, 2350, 2490),
    (7, 2490, 2660),
    (8, 2660, 2820),
    (9, 2820, 3000),
    (10, 3000, 3140),
    (11, 4100, 4260),
    (12, 4260, 4400),
    (13, 4400, 4540),
    (14, 4540, 4680),
    (15, 4680, 4830),
    (16, 4830, 5000),
    (17, 5000, 5170),
    (18, 5170, 5300),
    (19, 5300, 5430),
]

row_maps = {}

for r_num, start_idx, end_idx in row_ranges:
    r_data = {'num': r_num}
    
    # Collect all items in this range
    items = []
    for i in range(start_idx, end_idx):
        tag = doc.records[i]['tag']
        txt = get_txt(i)
        p = get_pos(i)
        k = get_kern(i)
        c = get_color(i)
        items.append({
            'idx': i,
            'tag': tag,
            'txt': txt,
            'pos': p,
            'kern': k,
            'col': c
        })
    
    print(f"\n=================== ROW {r_num} ===================")
    for it in items:
        if it['txt'] or it['tag'] in (150, 2100, 2206):
            extra = f"pos={it['pos']}" if it['pos'] else (f"kern={it['kern']}" if it['kern'] else (f"col={it['col']}" if it['col'] else ""))
            print(f"  Rec {it['idx']:4d} (Tag {it['tag']:4d}): {repr(it['txt'])} {extra}")

