import json
import struct
from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

def get_text(idx):
    if 0 <= idx < len(doc.records):
        r = doc.records[idx]
        if r['tag'] in (2201, 2202, 2203):
            return r['payload'].decode('utf-16le', errors='ignore')
    return ""

# Let's inspect the exact sequence of records for each row
row_starts = [
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

for row_num, start_idx, end_idx in row_starts:
    print(f"\n=================== ROW {row_num} (Rec {start_idx} to {end_idx}) ===================")
    for idx in range(start_idx, end_idx):
        r = doc.records[idx]
        tag = r['tag']
        txt = get_text(idx)
        if tag in (2201, 2202, 2203):
            print(f"  Rec {idx:4d} (Tag {tag:4d}): TEXT {repr(txt)}")
        elif tag == 150:
            print(f"  Rec {idx:4d} (Tag 150): COLOR {r['payload'].hex()}")
        elif tag == 2100:
            coords = struct.unpack('<iii', r['payload'][:12])
            print(f"  Rec {idx:4d} (Tag 2100): POS x={coords[0]}, y={coords[1]}")
        elif tag == 2206:
            metrics = struct.unpack('<iii', r['payload'][:12])
            print(f"  Rec {idx:4d} (Tag 2206): KERN w={metrics[0]}, h={metrics[1]}")
        elif tag == 2204:
            trans = struct.unpack('<ii', r['payload'][:8])
            print(f"  Rec {idx:4d} (Tag 2204): MATRIX dx={trans[0]}, dy={trans[1]}")
