import os
import json
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
doc = XarDocument(xar_path)
print(f"Loaded 0.xar with {len(doc.records)} records.")

# Helper to inspect record range
def get_text(idx):
    r = doc.records[idx]
    try:
        return r['payload'].decode('utf-16le')
    except:
        return ""

def find_text_records(keyword):
    matches = []
    for i, r in enumerate(doc.records):
        if r['tag'] in (2201, 2202, 2208, 2209):
            txt = get_text(i)
            if keyword.lower() in txt.lower():
                matches.append((i, r['tag'], txt))
    return matches

print("--- SEARCHING HEADERS ---")
print("Name matches:", find_text_records("Masriyah") or find_text_records("YULIANA") or find_text_records("ANWAR") or find_text_records("DINI") or find_text_records("ASEP"))
print("Periode matches:", find_text_records("Sep 2025") or find_text_records("2025") or find_text_records("2026"))
print("Dicetak matches:", find_text_records("Dicetak pada"))
print("Rekening matches:", find_text_records("15500") or find_text_records("16300") or find_text_records("14000"))
