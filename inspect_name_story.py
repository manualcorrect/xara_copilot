import os
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
doc = XarDocument(xar_path)

print("--- NAME / CABANG INVESTIGATION ---")
for idx in [3083, 5945, 8964]:
    print(f"\nContext around {idx}:")
    for j in range(idx - 15, idx + 10):
        r = doc.records[j]
        tag = r['tag']
        payload = r['payload']
        txt = ""
        if tag in (2201, 2202, 2208, 2209):
            try:
                txt = payload.decode('utf-16le')
            except:
                pass
        print(f"Rec {j:05d} (Tag {tag}, size={len(payload)}): {repr(txt)} {payload[:8].hex()}")

print("\n--- PAGE 1 CABANG CONTEXT around 935 ---")
for j in range(920, 955):
    r = doc.records[j]
    tag = r['tag']
    payload = r['payload']
    txt = ""
    if tag in (2201, 2202, 2208, 2209):
        try:
            txt = payload.decode('utf-16le')
        except:
            pass
    print(f"Rec {j:05d} (Tag {tag}, size={len(payload)}): {repr(txt)}")

print("\n--- PAGE 2 CABANG CONTEXT around 3596 ---")
for j in range(3580, 3615):
    r = doc.records[j]
    tag = r['tag']
    payload = r['payload']
    txt = ""
    if tag in (2201, 2202, 2208, 2209):
        try:
            txt = payload.decode('utf-16le')
        except:
            pass
    print(f"Rec {j:05d} (Tag {tag}, size={len(payload)}): {repr(txt)}")

print("\n--- PAGE 3 CABANG CONTEXT around 6458 ---")
for j in range(6445, 6475):
    r = doc.records[j]
    tag = r['tag']
    payload = r['payload']
    txt = ""
    if tag in (2201, 2202, 2208, 2209):
        try:
            txt = payload.decode('utf-16le')
        except:
            pass
    print(f"Rec {j:05d} (Tag {tag}, size={len(payload)}): {repr(txt)}")
