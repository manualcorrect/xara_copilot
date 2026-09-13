from xar_dom_engine import XarDocument

agu = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar')

print("Page 2 objects (4497..5282):")
for i in range(4497, 5282):
    r = agu.records[i]
    if r['tag'] in (104, 2000, 2100, 4498, 4463, 4465, 2200):
        print(f"Rec {i:5d}: Tag {r['tag']}")
