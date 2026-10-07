import sys
import json
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

# Page 1 Rows: 1..10 (Rec 1500..3150)
# Page 2 Rows: 11..15 (Rec 4100..4900)

row_nums = [
    (1, 1577), (2, 1749), (3, 1881), (4, 2073), (5, 2225),
    (6, 2352), (7, 2537), (8, 2684), (9, 2821), (10, 2987),
    (11, 4175), (12, 4332), (13, 4469), (14, 4616), (15, 4733)
]

for idx in range(len(row_nums)):
    r_num, start_rec = row_nums[idx]
    end_rec = row_nums[idx+1][1] if idx+1 < len(row_nums) else 4850
    print(f"\n=================== ROW {r_num:2d} (Rec {start_rec}..{end_rec}) ===================")
    for i in range(start_rec, end_rec):
        txt = get_txt(i)
        tag = doc.records[i]['tag']
        if txt or tag in (150, 2100, 2206, 2204):
            p = get_pos(i)
            k = get_kern(i)
            c = get_color(i)
            extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
            print(f"  Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}")

