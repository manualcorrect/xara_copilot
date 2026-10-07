from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar')

print("=== NATIVE ATTRIBUTES IN 0.xar FOR NAME & HEADERS ===")
# Check record 964 to 990 (Page 1 Name & Cabang)
for j in range(964, 990):
    r = doc.records[j]
    info = ""
    if r['tag'] == 150:
        val = struct.unpack('<i', r['payload'])[0]
        info = f" | Tag 150 COLOR = {val} (hex: {r['payload'].hex()})"
    elif r['tag'] == 2907:
        val = struct.unpack('<i', r['payload'])[0]
        info = f" | Tag 2907 FONT = {val} (hex: {r['payload'].hex()})"
    elif r['tag'] == 2906:
        val = struct.unpack('<i', r['payload'])[0]
        info = f" | Tag 2906 STYLE = {val} (hex: {r['payload'].hex()})"
    elif r['tag'] == 2901:
        val = struct.unpack('<i', r['payload'])[0]
        info = f" | Tag 2901 SIZE = {val} (hex: {r['payload'].hex()})"
    elif r['tag'] == 2150:
        w, fl = struct.unpack('<iB', r['payload'])
        info = f" | Tag 2150 WIDTH = {w} mp ({w/28346.4567:.3f}cm), flag={fl}"
    elif r['tag'] == 2100:
        c = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        info = f" | Tag 2100 COORDS = {c} (X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm)"
    elif r['tag'] in (2201, 2202):
        info = " | TEXT = " + repr(r['payload'].decode('utf-16le', errors='ignore'))
    print(f"[{j}] Tag {r['tag']} (sz {r['size']}): {r['payload'].hex()}{info}")
