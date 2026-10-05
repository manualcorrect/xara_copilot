import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar")

for i in range(1090, 1170):
    r = doc.records[i]
    tag = r['tag']
    p = r['payload']
    if tag == 150:
        print(f"Rec {i:05d} (Tag 150): {p.hex()}")
    elif tag in (2201, 2202):
        print(f"Rec {i:05d} (Tag {tag}): {repr(p.decode('utf-16le'))}")
    elif tag == 2100 and len(p) >= 12:
        x, y, f = struct.unpack('<iii', p[:12])
        print(f"Rec {i:05d} (Tag 2100): x={x}, y={y}")
