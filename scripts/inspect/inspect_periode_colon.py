from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar')

for i in range(850, 1040):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        print(f"[{i}] Tag {r['tag']}: {r['payload'].decode('utf-16le', errors='ignore')!r}")
    elif r['tag'] == 2100:
        coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        print(f"[{i}] Tag 2100: coords={coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)")
