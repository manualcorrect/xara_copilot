import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Let's inspect all Tag 2100 positions
positions = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2100:
        x, y, p = struct.unpack('<iii', r['payload'][:12])
        positions.append((i, x, y, p))

# Find all text nodes before or after tag 2100
print("Total Tag 2100 positions:", len(positions))

# Let's find all nominal and saldo candidates by looking for numbers with ',' or '.'
amounts = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(c.isdigit() for c in txt) and (',' in txt or '.' in txt or txt.startswith('+') or txt.startswith('-')):
                # Find nearest Tag 2100
                nearest_2100 = None
                for j in range(i, min(len(doc.records), i+15)):
                    if doc.records[j]['tag'] == 2100:
                        nearest_2100 = struct.unpack('<iii', doc.records[j]['payload'][:12])
                        break
                amounts.append((i, r['tag'], txt, nearest_2100))
        except:
            pass

print(f"\nFound {len(amounts)} amount nodes:")
for a in amounts:
    print(f"Rec {a[0]:4d} (Tag {a[1]}): '{a[2]}' | 2100={a[3]}")
