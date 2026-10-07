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

row_boundaries = [
    (1, 1521, 1694),
    (2, 1694, 1856),
    (3, 1856, 2028),
    (4, 2028, 2205),
    (5, 2205, 2382),
    (6, 2382, 2509),
    (7, 2509, 2676),
    (8, 2676, 2892),
    (9, 2892, 3029),
    (10, 3029, 3140),
    (11, 4138, 4282),
    (12, 4282, 4424),
    (13, 4424, 4566),
    (14, 4566, 4713),
    (15, 4713, 4885),
    (16, 4885, 5007),
    (17, 5007, 5200),
    (18, 5200, 5312),
    (19, 5312, 5430)
]

for r_num, s_idx, e_idx in row_boundaries:
    txts = []
    for i in range(s_idx, e_idx):
        t = get_txt(i)
        if t:
            txts.append((i, doc.records[i]['tag'], t))
    print(f"\n--- ROW {r_num} (Rec {s_idx}..{e_idx}) ---")
    for idx, tag, txt in txts:
        print(f"  Rec {idx:4d} (Tag {tag:4d}): {repr(txt)}")

