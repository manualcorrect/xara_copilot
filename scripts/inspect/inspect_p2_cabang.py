import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("--- CABANG ON PAGE 2 (Around Record 5870-5900) ---")
for idx in range(5865, 5898):
    r = doc.records[idx]
    print(f"[{idx}] Tag {r['tag']} (size {r['size']}): {r['payload'].hex()}")
    if r['tag'] == 2201:
        print("    Text:", repr(r['payload'].decode('utf-16le', errors='ignore')))
    elif r['tag'] == 2206:
        vals = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        print(f"    Kern/Lead: {vals}")
    elif r['tag'] == 2100:
        coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        print(f"    Coords: {coords} -> X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm")
    elif r['tag'] == 2150:
        w, flag = struct.unpack('<iB', r['payload'])
        print(f"    Col Width: {w} mp ({w/28346.4567:.3f} cm)")
