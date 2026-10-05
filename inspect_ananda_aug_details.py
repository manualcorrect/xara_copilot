import sys
import json
import struct
from xar_dom_engine import XarDocument

sys.stdout.reconfigure(encoding='utf-8')

aug_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Aug"
xar_path = f"{aug_dir}\\0.xar"
doc = XarDocument(xar_path)

print(f"Total records in Aug 0.xar: {len(doc.records)}")

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

# Find all text nodes
text_nodes = []
for i, r in enumerate(doc.records):
    txt = get_txt(i)
    if txt.strip():
        text_nodes.append((i, r['tag'], txt))

print(f"Total Text Nodes: {len(text_nodes)}")
with open('ananda_aug_texts.json', 'w', encoding='utf-8') as f:
    json.dump([{'idx': i, 'tag': tag, 'text': txt} for i, tag, txt in text_nodes], f, indent=2, ensure_ascii=False)

# Let's inspect candidate row numbers
row_cands = []
for i, tag, txt in text_nodes:
    if txt in [str(n) for n in range(1, 25)]:
        row_cands.append((i, tag, txt))

print("Candidate row numbers:")
for i, tag, txt in row_cands:
    print(f"  Rec {i:4d} (Tag {tag:4d}): {repr(txt)}")

# Find all amount text nodes
print("\nAmount text nodes:")
for i, tag, txt in text_nodes:
    if ',00' in txt or ',0' in txt or (txt.startswith('-') or txt.startswith('+')):
        print(f"  Rec {i:4d} (Tag {tag:4d}): {repr(txt)}")

