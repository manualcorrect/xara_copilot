import struct
from xar_dom_engine import XarDocument

jun = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap7.xar')
agu = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar')

print("=== JUN TAG 2100 AROUND ADDRESS ===")
for i in range(250, 350):
    r = jun.records[i]
    if r['tag'] in (2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2200, 2206):
        vals = ""
        if len(r['payload']) >= 12:
            vals = struct.unpack("<iii", r['payload'][:12])
        elif len(r['payload']) >= 8:
            vals = struct.unpack("<ii", r['payload'][:8])
        print(f"Jun {i:4d}: Tag {r['tag']} | payload_len={len(r['payload'])} | {vals}")

print("\n=== AGU TAG 2100 AROUND ADDRESS ===")
for i in range(250, 460):
    r = agu.records[i]
    if r['tag'] in (2100, 2101, 2102, 2103, 2104, 2105, 2106, 2107, 2108, 2109, 2110, 2200, 2206):
        vals = ""
        if len(r['payload']) >= 12:
            vals = struct.unpack("<iii", r['payload'][:12])
        elif len(r['payload']) >= 8:
            vals = struct.unpack("<ii", r['payload'][:8])
        print(f"Agu {i:4d}: Tag {r['tag']} | payload_len={len(r['payload'])} | {vals}")
