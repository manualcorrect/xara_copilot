import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== PAGE 1 NAME & CABANG (Records 950 to 1005) ===")
for idx in range(950, 1005):
    rec = doc.records[idx]
    info = ""
    if rec['tag'] in (2201, 2202):
        info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
    elif rec['tag'] == 2100:
        coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
    elif rec['tag'] == 2150:
        w, flag = struct.unpack('<iB', rec['payload'])
        info = f" | col width: {w} mp ({w/28346.4567:.3f}cm)"
    elif rec['tag'] == 2206:
        vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | kern/lead: {vals}"
    elif rec['tag'] == 2901:
        sz = struct.unpack('<i', rec['payload'])[0]
        info = f" | font size: {sz} mp ({sz/1000:.1f}pt)"
    elif rec['tag'] in (4208, 4209):
        val = struct.unpack('<i', rec['payload'])[0]
        info = f" | line pitch: {val} ({val/500*100}%)"
    print(f"[{idx}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()[:30]}{info}")
