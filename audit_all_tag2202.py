from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0_ORIGINAL_BACKUP.xar")

for i, r in enumerate(doc.records):
    if r['tag'] == 2202:
        try:
            txt = r['payload'].decode('utf-16le')
        except:
            txt = '<raw>'
        print(f"Rec {i:05d} (Tag 2202, size={len(r['payload'])}): {repr(txt)}")
