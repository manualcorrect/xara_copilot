from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar')
print("--- SEARCHING CUSTOMER NAME RECORDS IN 0_tahap7.xar ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if any(w in t.lower() for w in ['masriyah', 'marsiyah', 'samian', 'muhammad', 'firmansyah', 'bendi']):
            print(f"Rec {i:5d} [Tag {r['tag']}]: '{t}'")
