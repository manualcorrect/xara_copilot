import struct
from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

for r in range(1885, 1940):
    rec = doc.records[r]
    tag = rec['tag']
    sz = rec['size']
    txt = rec['payload'].decode('utf-16le', errors='ignore') if tag in (2201, 2202, 2203) else ''
    p12 = struct.unpack('<iii', rec['payload'][:12]) if sz >= 12 else None
    print(f"Rec {r:4d} (Tag {tag:4d}, sz={sz:2d}): {repr(txt)} {p12 if tag in (2100, 2206) else ''}")

