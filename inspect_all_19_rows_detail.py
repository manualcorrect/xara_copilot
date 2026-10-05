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

with open('all_19_rows_utf8.txt', 'w', encoding='utf-8') as out:
    # Page 1 Rows (1500 to 3140)
    out.write("=== PAGE 1 ROWS (1500..3140) ===\n")
    for i in range(1500, 3140):
        txt = get_txt(i)
        tag = doc.records[i]['tag']
        if txt or tag in (150, 2100, 2206, 2204):
            p = get_pos(i)
            k = get_kern(i)
            c = get_color(i)
            extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
            out.write(f"Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}\n")

    # Page 2 Rows (4100 to 5430)
    out.write("\n=== PAGE 2 ROWS (4100..5430) ===\n")
    for i in range(4100, 5430):
        txt = get_txt(i)
        tag = doc.records[i]['tag']
        if txt or tag in (150, 2100, 2206, 2204):
            p = get_pos(i)
            k = get_kern(i)
            c = get_color(i)
            extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
            out.write(f"Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}\n")

print("Saved all_19_rows_utf8.txt")
