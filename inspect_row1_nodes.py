import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Let's inspect rows 1 to 22 individually
# Row 1:
print("=== DETAIL ROW 1 ===")
for i in range(1510, 1640):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        print(f"Rec {i:4d} | Tag {r['tag']} | TXT: {repr(r['payload'].decode('utf-16le').rstrip(chr(0)))}")
    elif r['tag'] == 2100:
        x, y, p = struct.unpack('<iii', r['payload'][:12])
        print(f"Rec {i:4d} | Tag 2100 | (x={x}, y={y})")
    elif r['tag'] == 2206:
        w, h, unk = struct.unpack('<iii', r['payload'][:12])
        print(f"Rec {i:4d} | Tag 2206 | (w={w}, h={h})")
    elif r['tag'] == 150:
        print(f"Rec {i:4d} | Tag  150 | col={r['payload'].hex()}")
