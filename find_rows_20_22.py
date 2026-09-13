import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Inspect all text nodes in rows 19, 20, 21, 22
for start, end, label in [(5600, 5820, 'Row 20 area'), (5800, 6010, 'Row 21 area'), (6000, 6200, 'Row 22 area')]:
    print(f"\n=== {label} ===")
    for i in range(start, end):
        r = doc.records[i]
        if r['tag'] in (2201, 2202):
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            y = None
            for j in range(i, min(len(doc.records), i+15)):
                if doc.records[j]['tag'] == 2100:
                    y = struct.unpack('<iii', doc.records[j]['payload'][:12])[1]
                    break
            print(f"Rec {i:4d} (Tag {r['tag']}): {repr(txt)} | Y={y}")
