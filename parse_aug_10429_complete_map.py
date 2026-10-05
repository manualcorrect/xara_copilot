import os
import json
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar"
doc = XarDocument(xar_path)

with open("aug_10429_texts_dump.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

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

print("=== LOCATING HEADERS IN AUG 0.XAR ===")
# Search name, periode, dicetak, rekening across pages
for t in texts:
    txt = t['text']
    idx = t['idx']
    if any(k in txt for k in ['YULIANA', 'Masriyah', 'ANWAR', 'DINI', 'PT BENDI', 'MASRIYAH']):
        print(f"Customer Name node: Rec {idx} (Tag {t['tag']}): {repr(txt)}")
    if 'Sep 2025' in txt or 'Aug 2025' in txt or 'Jul 2025' in txt or 'Okt 2025' in txt or 'Nov 2025' in txt:
        print(f"Date/Periode node: Rec {idx} (Tag {t['tag']}): {repr(txt)}")
    if '16300' in txt or '15500' in txt:
        print(f"Account/Rekening node: Rec {idx} (Tag {t['tag']}): {repr(txt)}")
    if 'dari 10' in txt or 'of 10' in txt or 'dari 3' in txt or 'of 3' in txt:
        print(f"Page Number node: Rec {idx} (Tag {t['tag']}): {repr(txt)}")
