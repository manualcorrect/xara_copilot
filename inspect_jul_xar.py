import struct
from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar'
doc = XarDocument(xar_path)
print(f"Total records: {len(doc.records)}")

# Let's inspect all text records (Tag 2201, 2202)
texts = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            texts.append((i, r['tag'], txt))
        except:
            pass

print(f"Total text nodes: {len(texts)}")

# 1. Search for headers
print("\n--- Potential Header / Name texts ---")
for i, tag, txt in texts:
    if any(w in txt.upper() for w in ['YULIANA', 'SANI', 'PUTRI', 'FIRMANSYAH', 'NOV 2025', 'DES 2025', 'OF 7', 'DARI 7', 'OF 3', 'DARI 3']):
        print(f"Rec {i} (Tag {tag}): '{txt}'")

# 2. Search for Account number
print("\n--- Potential Account / Summary texts ---")
for i, tag, txt in texts:
    if any(w in txt for w in ['1630', '163', '1094', '42426', '1.929', '9.197', '5.234', '5.891', '14000']):
        print(f"Rec {i} (Tag {tag}): '{txt}'")

# 3. Search for Row numbers 23, 24, 25, 30, 31, 32, 35, 36, 46
print("\n--- Row Numbers ---")
for i, tag, txt in texts:
    if txt.strip() in [str(n) for n in range(20, 50)]:
        print(f"Rec {i} (Tag {tag}): '{txt}'")

# 4. Search for Nominals / Saldos from image 2
print("\n--- Sample Transaction Nominals / Saldos ---")
for i, tag, txt in texts:
    if any(w in txt for w in ['397.500', '1.532.004', '500.000', '525.704', '551.967', '201.467', '71.467', '80.000', '105.000']):
        print(f"Rec {i} (Tag {tag}): '{txt}'")
