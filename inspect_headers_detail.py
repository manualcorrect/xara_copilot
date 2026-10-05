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

# Let's find every text node between 950 and 1350
print("--- Page 1 Header Text & Props ---")
for i in range(950, 1330):
    txt = get_txt(i)
    tag = doc.records[i]['tag']
    if txt or tag in (150, 2100, 2206, 2204):
        p = get_pos(i)
        k = get_kern(i)
        c = get_color(i)
        extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
        print(f"Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}")

print("\n--- Page 2 Header Text & Props ---")
for i in range(3720, 4100):
    txt = get_txt(i)
    tag = doc.records[i]['tag']
    if txt or tag in (150, 2100, 2206, 2204):
        p = get_pos(i)
        k = get_kern(i)
        c = get_color(i)
        extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
        print(f"Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}")

