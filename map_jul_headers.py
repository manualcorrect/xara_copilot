from xar_dom_engine import XarDocument
import struct

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

print("=" * 80)
print("INSPECTING JUL 0.XAR ALL 8 PAGES HEADERS & SUMMARY")
print("=" * 80)

# 1. Customer Name across all 8 pages
print("\n--- 1. Customer Name Nodes ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if 'ROY DARWIN' in t:
            # find preceding tag 2206
            k_rec = i - 1 if doc.records[i-1]['tag'] == 2206 else None
            w = struct.unpack('<iii', doc.records[k_rec]['payload'][:12])[0] if k_rec else None
            print(f"Rec {i:5d}: '{t}' | Tag 2206 Rec {k_rec}: width={w}")

# 2. Period across all 8 pages
print("\n--- 2. Period Nodes ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if 'Feb 202' in t or '01 Feb' in t:
            print(f"Rec {i:5d} [Tag {r['tag']}]: '{t}'")

# 3. Dicetak Pada across all 8 pages
print("\n--- 3. Dicetak Pada Nodes ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if 'Sep 2026' in t or '10 Sep' in t:
            print(f"Rec {i:5d} [Tag {r['tag']}]: '{t}'")

# 4. Account Number
print("\n--- 4. Account Number Nodes ---")
for i in range(700, 1100):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if any(c.isdigit() for c in t) and len(t) >= 6:
            print(f"Rec {i:5d} [Tag {r['tag']}]: '{t}'")

# 5. Financial Summary Header
print("\n--- 5. Financial Summary Header Nodes (Page 1) ---")
for i in range(1100, 1300):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if t:
            print(f"Rec {i:5d} [Tag {r['tag']}]: '{t}'")
