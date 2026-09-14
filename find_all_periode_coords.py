from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar')

print("=== ALL PERIODE / PERIOD / DATE OCCURRENCES ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if any(k in txt for k in ['Periode', 'Period', '01 Jul', '31 Jul']):
            # find preceding Tag 2100
            p2100 = "NONE"
            for k in range(i, max(0, i-30), -1):
                if doc.records[k]['tag'] == 2100:
                    coords = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]["payload"])
                    p2100 = f"Rec {k}: coords={coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
                    break
            print(f"Record [{i}] Tag {r['tag']}: {txt!r} | Preceding Tag 2100: {p2100}")
