import struct
from xar_dom_engine import XarDocument

jun = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap7.xar')
agu = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar')

print("--- JUN 170..205 ---")
for i in range(170, 205):
    r = jun.records[i]
    extra = ""
    if r['tag'] == 2100:
        extra = str(struct.unpack('<iii', r['payload'][:12]))
    print(f"Jun {i:3d}: Tag {r['tag']:4d} {extra}")

print("\n--- AGU 170..205 ---")
for i in range(170, 205):
    r = agu.records[i]
    extra = ""
    if r['tag'] == 2100:
        extra = str(struct.unpack('<iii', r['payload'][:12]))
    print(f"Agu {i:3d}: Tag {r['tag']:4d} {extra}")
