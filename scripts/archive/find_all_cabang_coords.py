import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print(f"Total records: {len(doc.records)}")

for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'KCP' in txt or 'Jakarta' in txt or 'Aries' in txt:
            print(f"\n[Record {i}] Tag {r['tag']}, Text: {repr(txt)}")
            # Find preceding Tag 2100
            for j in range(i, max(0, i - 25), -1):
                rec = doc.records[j]
                if rec['tag'] == 2100:
                    coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    print(f"  Preceding Tag 2100 at [{j}]: {coords} -> X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm")
                    break
                elif rec['tag'] == 2150:
                    w, flag = struct.unpack('<iB', rec['payload'])
                    print(f"  Tag 2150 at [{j}]: width={w} mp ({w/28346.4567:.3f}cm)")
