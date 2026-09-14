import struct
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== FINANCIAL SUMMARY HEADER RECORDS ON PAGE 1 ===")
for i in range(1160, 1260):
    r = doc.records[i]
    tag = r['tag']
    pl = r['payload']
    if tag in (2201, 2202):
        print(f"[{i:5d}] Tag {tag:4d}: TEXT  = {pl.decode('utf-16le', errors='ignore')!r}")
    elif tag == 150:
        print(f"[{i:5d}] Tag {tag:4d}: COLOR = {pl.hex()}")
    elif tag == 2206:
        print(f"[{i:5d}] Tag {tag:4d}: T2206 = {struct.unpack('<iii', pl[:12])}")
    elif tag == 2100:
        coords = struct.unpack(f'<{len(pl)//4}i', pl)
        print(f"[{i:5d}] Tag {tag:4d}: POS   = {coords}")
