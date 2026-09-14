from xar_dom_engine import XarDocument
import struct

base_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(base_xar)
print(f"Total records in pristine 0.xar: {len(doc.records):,}")

print("\n=== FONT DEFINITIONS IN 0.xar ===")
for i, r in enumerate(doc.records[:500]):
    if r['tag'] in (2900, 2905, 2906, 2907, 2908, 2909, 2910):
        hex_p = r['payload'].hex()
        txt = r['payload'].decode('utf-16le', errors='ignore') if len(r['payload']) > 4 else ""
        print(f"Rec [{i}] Tag {r['tag']} (sz {r['size']}): {hex_p} | text={txt!r}")

print("\n=== NAME & CABANG IN 0.xar (PAGES 1 to 3) ===")
for p in range(1, 4):
    for i, r in enumerate(doc.records):
        if r['tag'] == 2201 and ('ANWAR' in r['payload'].decode('utf-16le', errors='ignore') or 'DINI' in r['payload'].decode('utf-16le', errors='ignore') or 'MASRIYAH' in r['payload'].decode('utf-16le', errors='ignore') or 'Jakarta' in r['payload'].decode('utf-16le', errors='ignore')):
            start = max(0, i - 15)
            end = min(len(doc.records), i + 10)
            print(f"\n--- Occurrence at Rec [{i}] ---")
            for j in range(start, end):
                rec = doc.records[j]
                info = ""
                if rec['tag'] in (2201, 2202):
                    info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
                elif rec['tag'] == 2100:
                    c = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    info = f" | coords: {c} (X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm)"
                elif rec['tag'] == 2150:
                    w, fl = struct.unpack('<iB', rec['payload'])
                    info = f" | W={w} mp ({w/28346.4567:.3f}cm)"
                elif rec['tag'] == 2206:
                    vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    info = f" | kern/lead: {vals}"
                elif rec['tag'] == 2907:
                    val = struct.unpack('<i', rec['payload'])[0]
                    info = f" | font_ref={val}"
                elif rec['tag'] == 150:
                    val = struct.unpack('<i', rec['payload'])[0]
                    info = f" | color_ref={val}"
                print(f"  [{j}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()[:30]}{info}")
            break
