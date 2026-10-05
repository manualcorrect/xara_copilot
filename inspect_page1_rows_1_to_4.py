import os
import json
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
doc = XarDocument(xar_path)

print("=== INSPECTING PAGE 1 NODES BETWEEN 1400 AND 2000 ===")
for i in range(1400, 2000):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        try:
            txt = r['payload'].decode('utf-16le')
            print(f"Rec {i:05d} (Tag {r['tag']:4d}, size={len(r['payload']):2d}): {repr(txt)}")
        except:
            pass
