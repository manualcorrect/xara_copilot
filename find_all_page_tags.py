from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar')

print("=== ALL SPREAD / CHAPTER / PAGE TAGS ===")
for i, r in enumerate(doc.records):
    # Tag 2000 = TAG_PAGE, Tag 2001 = TAG_SPREAD, Tag 2002 = TAG_CHAPTER
    if r['tag'] in range(2000, 2010):
        print(f"Rec {i:5d}: Tag {r['tag']} (Size {r['size']})")
