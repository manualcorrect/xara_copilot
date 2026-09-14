from xar_dom_engine import XarDocument
import struct

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

print(f"Total records in 0.xar: {len(doc.records):,}")

# Find all pages in 0.xar
# In Xara documents, each page has Tag 4465 or 'Page X of Y' / 'X of Y'
page_defs = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if any(w in t.lower() for w in ['of ', 'dari ', 'page ']):
            page_defs.append((i, r['tag'], t))

print("\n--- PAGE NUMBER RECORDS ---")
for i, tag, t in page_defs:
    print(f"Rec {i:5d} [Tag {tag}]: '{t}'")

# Find customer name records
print("\n--- CUSTOMER NAME / HEADER RECORDS ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if any(w in t for w in ['ROY', 'DARWIN', 'MASRIYAH', 'Masriyah', 'SAMIAN', '163001', 'Dicetak', 'Periode', 'Period', 'Issued', 'Initial Balance', 'Saldo Awal', 'Closing']):
            print(f"Rec {i:5d} [Tag {r['tag']}]: '{t}'")

# Count table transaction rows in 0.xar
row_dates = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if '2026' in t and any(m in t for m in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']):
            row_dates.append((i, t))

print(f"\n--- TRANSACTION DATE RECORDS (Total: {len(row_dates)}) ---")
for i, t in row_dates[:20]:
    print(f"Rec {i:5d}: '{t}'")
if len(row_dates) > 20:
    print(f"... and {len(row_dates) - 20} more date records ...")
    for i, t in row_dates[-5:]:
        print(f"Rec {i:5d}: '{t}'")
