import sys
import struct
from xar_dom_engine import XarDocument

sys.stdout.reconfigure(encoding='utf-8')

aug_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Aug"
xar_path = f"{aug_dir}\\0.xar"
doc = XarDocument(xar_path)

def get_txt(idx):
    if 0 <= idx < len(doc.records):
        r = doc.records[idx]
        if r['tag'] in (2201, 2202, 2203):
            return r['payload'].decode('utf-16le', errors='ignore')
    return ""

row_ranges = [
    (1, 1577, 1749),
    (2, 1749, 1881),
    (3, 1881, 2073),
    (4, 2073, 2225),
    (5, 2225, 2352),
    (6, 2352, 2537),
    (7, 2537, 2684),
    (8, 2684, 2821),
    (9, 2821, 2987),
    (10, 2987, 3140),
    (11, 4175, 4332),
    (12, 4332, 4469),
    (13, 4469, 4616),
    (14, 4616, 4733),
    (15, 4733, 4880)
]

for r_num, s_idx, e_idx in row_ranges:
    txts = []
    for i in range(s_idx, e_idx):
        t = get_txt(i)
        if t:
            txts.append((i, doc.records[i]['tag'], t))
    print(f"\n--- ROW {r_num:2d} (Rec {s_idx}..{e_idx}) ---")
    for idx, tag, txt in txts:
        print(f"  Rec {idx:4d} (Tag {tag:4d}): {repr(txt)}")

