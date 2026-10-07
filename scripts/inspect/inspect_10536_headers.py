import os
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
doc = XarDocument(xar_path)

def get_text(idx):
    try:
        return repr(doc.records[idx]['payload'].decode('utf-16le'))
    except:
        return "<raw>"

print("--- PAGE 1 HEADER NODES (around 300 - 1300) ---")
for i in range(300, 1300):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        print(f"Rec {i:05d} (Tag {r['tag']}): {get_text(i)}")

print("\n--- PAGE 2 HEADER NODES (around 3300 - 4000) ---")
for i in range(3300, 4000):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        print(f"Rec {i:05d} (Tag {r['tag']}): {get_text(i)}")

print("\n--- PAGE 3 HEADER NODES (around 6200 - 6800) ---")
for i in range(6200, 6800):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        print(f"Rec {i:05d} (Tag {r['tag']}): {get_text(i)}")
