import struct
from xar_dom_engine import XarDocument

agu = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar')

print('=== AGU PAGE 1 (305..436) ===')
for i in range(305, 436):
    r = agu.records[i]
    tag = r['tag']
    if tag in (2201, 2202):
        print(f'{i:4d} Tag {tag:4d}: {repr(r["payload"].decode("utf-16le", errors="ignore"))}')
    elif tag == 2204:
        print(f'{i:4d} Tag 2204: {struct.unpack("<ii", r["payload"][:8])}')
    elif tag == 2206:
        print(f'{i:4d} Tag 2206: {struct.unpack("<iii", r["payload"][:12])}')
