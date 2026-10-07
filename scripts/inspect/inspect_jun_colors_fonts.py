from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

# Fonts
fonts = set()
for r in doc.records:
    if r['tag'] == 2907:
        fonts.add(r['payload'].hex())

# Colors
colors = {}
for r in doc.records:
    if r['tag'] == 150:
        h = r['payload'].hex()
        colors[h] = colors.get(h, 0) + 1

print("=== JUN 0.XAR ATTRIBUTES ===")
print("Active Font IDs:", fonts)
print("Active Color IDs:", colors)
