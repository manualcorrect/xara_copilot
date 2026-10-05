import json
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar")

# Let's inspect between 3000 and 4200, and between 8500 and 8850
print("=== INSPECTING NODES 3000 TO 4200 (Page 1 bottom to Page 2 top) ===")
for i in range(3050, 4200):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        try:
            txt = r['payload'].decode('utf-16le')
            if txt.strip():
                print(f"Rec {i:05d} (Tag {r['tag']:4d}, size={len(r['payload']):2d}): {repr(txt)}")
        except:
            pass

print("\n=== INSPECTING NODES 8500 TO 8850 (Page 3 bottom) ===")
for i in range(8500, 8850):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        try:
            txt = r['payload'].decode('utf-16le')
            if txt.strip():
                print(f"Rec {i:05d} (Tag {r['tag']:4d}, size={len(r['payload']):2d}): {repr(txt)}")
        except:
            pass
