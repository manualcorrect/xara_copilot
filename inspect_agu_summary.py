from xar_dom_engine import XarDocument

agu_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar'
doc = XarDocument(agu_xar)

print("=== ACCOUNT & SUMMARY SECTION (Rec 1560 - 1800) ===")
for i in range(1560, 1800):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            print(f"Rec {i:5d} (Tag {r['tag']}, Size {r['size']}): '{txt}'")
        except:
            pass
