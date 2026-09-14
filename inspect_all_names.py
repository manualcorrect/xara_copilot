import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)
print(f"Total records: {len(doc.records)}")

for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'MASRIYAH' in txt:
            print(f"\nRecord {i}: Tag {r['tag']}, Text: {repr(txt)}")
            start = max(0, i - 15)
            end = min(len(doc.records), i + 15)
            for j in range(start, end):
                rec = doc.records[j]
                hex_p = rec['payload'].hex()
                # If text
                info = ""
                if rec['tag'] == 2201:
                    info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
                elif rec['tag'] == 2150:
                    w, flag = struct.unpack('<iB', rec['payload'])
                    info = f" | col width: {w} mp ({w/28346.4567:.3f} cm), flag: {flag}"
                elif rec['tag'] == 2100:
                    coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    info = f" | coords: {coords}"
                elif rec['tag'] == 2206:
                    vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    info = f" | kern/lead: {vals}"
                print(f"  [{j}] Tag {rec['tag']} (len {rec['size']}): {hex_p}{info}")
            print('='*60)
