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

print("=== ROW 15 RECORDS (4730..4880) ===")
for i in range(4730, 4880):
    txt = get_txt(i)
    tag = doc.records[i]['tag']
    if txt or tag in (150, 2100, 2206, 2204):
        p = get_pos(i)
        k = get_kern(i)
        c = get_color(i)
        extra = f"pos={p}" if p else (f"kern={k}" if k else (f"col={c}" if c else ""))
        print(f"Rec {i:4d} (Tag {tag:4d}): {repr(txt)} {extra}")

