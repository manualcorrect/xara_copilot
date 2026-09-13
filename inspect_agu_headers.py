from xar_dom_engine import XarDocument

agu_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar'
doc = XarDocument(agu_xar)

for i in range(min(1500, len(doc.records))):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if len(txt.strip()) > 1:
                print(f"Rec {i:4d} (Tag {r['tag']}): '{txt}'")
        except:
            pass
