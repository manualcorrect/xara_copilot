from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar")

print("=== NODES 7070 TO 7140 ===")
for i in range(7070, 7140):
    r = doc.records[i]
    tag = r['tag']
    p = r['payload']
    txt = ''
    if tag in (2201, 2202, 2208, 2209):
        try:
            txt = p.decode('utf-16le')
        except:
            pass
    if txt or tag in (150, 2100, 2200, 2203, 2206):
        print(f"Rec {i:05d} (Tag {tag:4d}, size={len(p):2d}): {repr(txt)}")
