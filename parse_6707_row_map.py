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

# Let's write an automated row boundary detector and mapper
# We know the rows:
# Page 1: Rows 1..10
# Page 2: Rows 11..19

# Let's search all records for nominal patterns (e.g. contain ',00' or similar) and saldo patterns
amounts = []
for i, r in enumerate(doc.records):
    txt = get_txt(i)
    if ',00' in txt or ',0' in txt:
        amounts.append((i, r['tag'], txt))

print(f"Total amount text nodes found: {len(amounts)}")
for idx, tag, txt in amounts:
    print(f"Rec {idx:4d} (Tag {tag:4d}): {repr(txt)}")

