from xar_dom_engine import XarDocument
import struct

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

print("=" * 80)
print("INSPECTING ALL TRANSACTION ROWS IN 0.XAR (JULY)")
print("=" * 80)

# In Xara, each row has a row number, date, time, description, nominal, saldo
# Let's search all Tag 2201/2202 text nodes and group by page
# Let's find page boundaries
page_divs = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if t in ['1 of 8', '2 of 8', '3 of 8', '4 of 8', '5 of 8', '6 of 8', '7 of 8', '8 of 8'] or 'of 8' in t:
            page_divs.append((i, t))

print(f"Page divisions found: {len(page_divs)}")
for idx, t in page_divs:
    print(f"  Rec {idx:5d}: '{t}'")

# Search all row numbers in 0.xar
row_numbers = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if t.isdigit() and 1 <= int(t) <= 100:
            # check if following node is saldo or kern
            is_row = False
            for k in range(i+1, min(len(doc.records), i+6)):
                if doc.records[k]['tag'] in (2204, 2206):
                    is_row = True
                    break
            if is_row:
                row_numbers.append((i, int(t), t))

print(f"\nTotal potential row numbers found: {len(row_numbers)}")
for i, num, t in row_numbers[:30]:
    print(f"  Rec {i:5d}: Row {num}")
if len(row_numbers) > 30:
    print(f"  ... and {len(row_numbers) - 30} more rows ...")
    for i, num, t in row_numbers[-10:]:
        print(f"  Rec {i:5d}: Row {num}")
