from xar_dom_engine import XarDocument
import openpyxl

agu_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar'
doc = XarDocument(agu_xar)

print(f"Loaded Agu 0.xar ({len(doc.records)} records)")

# 1. Inspect all occurrences of Name YULIANA / SANI / PUTRI
print("\n--- 1. NAMA NASABAH NODES ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(w in txt for w in ['YULIAN', 'SANI', 'PUTR']):
                print(f"Rec {i:5d} (Tag {r['tag']}): '{txt}'")
        except:
            pass

# 2. Inspect Periode Nodes (Nov 2025 / 30 / 01)
print("\n--- 2. PERIODE NODES ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(w in txt for w in ['Nov', '2025', '2026', 'v 202']):
                print(f"Rec {i:5d} (Tag {r['tag']}): '{txt}'")
        except:
            pass

# 3. Inspect Dicetak Pada Nodes
print("\n--- 3. DICETAK PADA NODES ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(w in txt for w in ['Des', 'Dec', 'Jan', 'Feb', 'Sep', '2025', '2026', '2027']):
                # check if near dicetak
                if i < 2500 or (5000 < i < 7000) or (9000 < i < 11000):
                    print(f"Rec {i:5d} (Tag {r['tag']}): '{txt}'")
        except:
            pass

# 4. Inspect Nomor Rekening & Halaman
print("\n--- 4. NOMOR REKENING & HALAMAN ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(w in txt for w in ['163', '1400', 'of ', 'dari ']):
                print(f"Rec {i:5d} (Tag {r['tag']}): '{txt}'")
        except:
            pass
