import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== ALL PERIOD DATE STORIES ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if '01 Jul 2026' in txt or ('Jul 2026' in txt and '-' in txt):
            # Print story from Tag 2100 before this to Tag 2203
            # Find preceding Tag 2100
            start = i
            for k in range(i, max(0, i-25), -1):
                if doc.records[k]['tag'] == 2100:
                    start = k
                    break
            # Find end Tag 2203
            end = i
            for k in range(i, min(len(doc.records), i+15)):
                if doc.records[k]['tag'] == 2203:
                    end = k + 2
                    break
            print(f"\n--- Period Story around record {i} (records {start}..{end}) ---")
            for idx in range(start, end+1):
                rec = doc.records[idx]
                info = ""
                if rec['tag'] in (2201, 2202):
                    info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
                elif rec['tag'] == 2100:
                    coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
                print(f"  [{idx}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()[:30]}{info}")
