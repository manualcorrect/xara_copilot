import os
import json
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar"
doc = XarDocument(xar_path)
print(f"Loaded Aug 0.xar with {len(doc.records)} records.")

def decode_text(p):
    try:
        return p.decode('utf-16le').strip()
    except:
        return ""

def get_tag150(idx):
    for j in range(idx - 1, max(0, idx - 25), -1):
        if doc.records[j]['tag'] == 150:
            return j
    return None

def get_tag2100(idx):
    for j in range(idx - 1, max(0, idx - 25), -1):
        if doc.records[j]['tag'] == 2100:
            return j
    return None

def get_tag2206(idx):
    for j in range(idx - 1, max(0, idx - 10), -1):
        if doc.records[j]['tag'] == 2206:
            return j
    return None

def get_tag2204(idx):
    for j in range(idx - 1, max(0, idx - 10), -1):
        if doc.records[j]['tag'] == 2204:
            return j
    return None

# Dump all text records
texts = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202, 2208, 2209):
        txt = decode_text(r['payload'])
        if txt:
            texts.append((i, r['tag'], txt, len(r['payload'])))

print(f"Total non-empty text records: {len(texts)}")

with open("aug_10429_texts_dump.json", "w", encoding="utf-8") as f:
    json.dump([{"idx": t[0], "tag": t[1], "text": t[2], "size": t[3]} for t in texts], f, indent=2)

print("Saved aug_10429_texts_dump.json.")
