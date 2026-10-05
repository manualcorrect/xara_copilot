import os
import json
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar"
doc = XarDocument(xar_path)

def get_txt(idx):
    try:
        return doc.records[idx]['payload'].decode('utf-16le')
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

# Let's inspect all text records between 1400 and 8850 to map all 36 rows
stories = []
for i in range(1200, 8850):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        txt = get_txt(i)
        stories.append({
            'idx': i,
            'tag': r['tag'],
            'text': txt,
            'tag150': get_tag150(i),
            'tag2100': get_tag2100(i),
            'tag2206': get_tag2206(i)
        })

print(f"Total stories extracted: {len(stories)}")
with open("aug_stories_extracted.json", "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2)
