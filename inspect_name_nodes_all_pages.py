from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar')

name_recs = [986, 3570, 6313, 9055, 11810, 14564, 17431]

for page_idx, r_idx in enumerate(name_recs, 1):
    print(f"\n--- Page {page_idx}: Name Record {r_idx} ---")
    for k in range(r_idx - 5, r_idx + 10):
        r = doc.records[k]
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if r['tag'] in (2201, 2202) else ''
        print(f"  Rec {k:5d} [Tag {r['tag']:4d}]: text='{t}' | size={r['size']}")
