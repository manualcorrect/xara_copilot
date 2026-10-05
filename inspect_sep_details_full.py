import sys
import json
import struct
from xar_dom_engine import XarDocument

sys.stdout.reconfigure(encoding='utf-8')

sep_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Sep"
xar_path = f"{sep_dir}\\0.xar"
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

print("=== INSPECTING HEADER PAGE 1 (900..1300) ===")
for i in range(900, 1300):
    txt = get_txt(i)
    tag = doc.records[i]['tag']
    if txt or tag in (150, 2100, 2206, 2204):
        p = get_pos(i)
        k = get_kern(i)
        c = get_color(i)
        extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
        print(f"Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}")

print("\n=== INSPECTING HEADER PAGE 2 (3600..4100) ===")
for i in range(3600, 4100):
    txt = get_txt(i)
    tag = doc.records[i]['tag']
    if txt or tag in (150, 2100, 2206, 2204):
        p = get_pos(i)
        k = get_kern(i)
        c = get_color(i)
        extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
        print(f"Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}")

print("\n=== INSPECTING ALL 13 ROWS ===")
row_ranges = [
    (1, 1497, 1664),
    (2, 1664, 1818),
    (3, 1818, 1950),
    (4, 1950, 2082),
    (5, 2082, 2276),
    (6, 2276, 2448),
    (7, 2448, 2590),
    (8, 2590, 2737),
    (9, 2737, 2907),
    (10, 2907, 3080),
    (11, 4083, 4237),
    (12, 4237, 4384),
    (13, 4384, 4550)
]

for r_num, s_idx, e_idx in row_ranges:
    print(f"\n--- ROW {r_num} (Rec {s_idx}..{e_idx}) ---")
    for i in range(s_idx, e_idx):
        txt = get_txt(i)
        tag = doc.records[i]['tag']
        if txt or tag in (150, 2100, 2206, 2204):
            p = get_pos(i)
            k = get_kern(i)
            c = get_color(i)
            extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
            print(f"  Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}")
