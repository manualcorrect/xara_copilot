import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== ALL PERIOD HEADERS ACROSS ALL PAGES ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Jul 2026' in txt and ('01' in txt or '31' in txt or '-' in txt or 'Periode' in txt):
            # Print preceding 10 records and next 5 records
            print(f"\nFound at Record [{i}] Tag {r['tag']}: {txt!r}")
            for j in range(max(0, i-8), min(len(doc.records), i+6)):
                rec = doc.records[j]
                t_txt = ""
                if rec['tag'] in (2201, 2202):
                    t_txt = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
                elif rec['tag'] == 2100:
                    coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    t_txt = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
                print(f"  [{j}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()[:30]}{t_txt}")
