from xar_dom_engine import XarDocument
import struct

tahap6_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap6.xar'
doc = XarDocument(tahap6_xar)
print(f"Total records in 0_tahap6.xar: {len(doc.records):,}")

print("\n=== NAME STORY IN 0_tahap6.xar (PAGE 1) ===")
for j in range(960, 995):
    rec = doc.records[j]
    info = ""
    if rec['tag'] in (2201, 2202):
        info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
    elif rec['tag'] == 2100:
        c = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | coords: {c} (X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm)"
    elif rec['tag'] == 2150:
        w, fl = struct.unpack('<iB', rec['payload'])
        info = f" | W={w} mp ({w/28346.4567:.3f}cm), flag={fl}"
    elif rec['tag'] == 2206:
        vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | kern/lead: {vals}"
    elif rec['tag'] == 2907:
        val = struct.unpack('<i', rec['payload'])[0]
        info = f" | font_ref={val}"
    elif rec['tag'] == 2901:
        val = struct.unpack('<i', rec['payload'])[0]
        info = f" | font_size={val}"
    elif rec['tag'] == 150:
        val = struct.unpack('<i', rec['payload'])[0]
        info = f" | color_ref={val}"
    print(f"[{j}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()}{info}")
