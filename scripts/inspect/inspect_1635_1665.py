from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

for k in range(1635, 1665):
    r = doc.records[k]
    t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if r['tag'] in (2201, 2202) else ''
    print(f"Rec {k:5d} [Tag {r['tag']:4d}]: size={r['size']:2d} | text='{t}' | hex={r['payload'].hex()[:20]}")
