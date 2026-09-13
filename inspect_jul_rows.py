import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Let's find all row number nodes: 23, 24, ..., 32, and 35, 36, ..., 46
target_nos = [str(n) for n in list(range(23, 33)) + list(range(35, 47))]

row_entries = []

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if txt.strip() in target_nos:
                # check if there's a Tag 2100 after it with Y coordinate
                y_coord = None
                for j in range(i, min(len(doc.records), i+15)):
                    if doc.records[j]['tag'] == 2100:
                        y_coord = struct.unpack('<iii', doc.records[j]['payload'][:12])[1]
                        break
                row_entries.append({'no_str': txt.strip(), 'rec_idx': i, 'y': y_coord})
        except:
            pass

print(f"Found {len(row_entries)} row number candidates:")
for re in row_entries:
    print(f"  Row {re['no_str']}: Rec {re['rec_idx']}, Y={re['y']}")
