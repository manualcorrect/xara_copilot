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

print("=== INSPECTING HEADER PAGE 1 (Around 900..1350) ===")
for i in range(900, 1350):
    r = doc.records[i]
    tag = r['tag']
    txt = get_txt(i)
    if tag in (2201, 2202, 2203):
        print(f"Rec {i:4d} (Tag {tag:4d}): TEXT {repr(txt)}")
    elif tag == 150:
        print(f"Rec {i:4d} (Tag 150): COLOR {r['payload'].hex()}")
    elif tag == 2100:
        pos = get_pos(i)
        print(f"Rec {i:4d} (Tag 2100): POS x={pos[0]}, y={pos[1]}")
    elif tag == 2206:
        kern = get_kern(i)
        print(f"Rec {i:4d} (Tag 2206): KERN w={kern[0]}, h={kern[1]}")

print("\n=== INSPECTING HEADER PAGE 2 (Around 3500..4150) ===")
for i in range(3500, 4150):
    r = doc.records[i]
    tag = r['tag']
    txt = get_txt(i)
    if tag in (2201, 2202, 2203):
        print(f"Rec {i:4d} (Tag {tag:4d}): TEXT {repr(txt)}")
    elif tag == 150:
        print(f"Rec {i:4d} (Tag 150): COLOR {r['payload'].hex()}")
    elif tag == 2100:
        pos = get_pos(i)
        print(f"Rec {i:4d} (Tag 2100): POS x={pos[0]}, y={pos[1]}")
    elif tag == 2206:
        kern = get_kern(i)
        print(f"Rec {i:4d} (Tag 2206): KERN w={kern[0]}, h={kern[1]}")
