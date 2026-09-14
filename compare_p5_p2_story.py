import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("--- PAGE 5 NAME STORY (Records 11838 to 11872) ---")
for idx in range(11838, 11873):
    r = doc.records[idx]
    print(f"[{idx}] Tag {r['tag']} (size {r['size']}): {r['payload'].hex()}")
    if r['tag'] == 2201:
        print("    Text:", repr(r['payload'].decode('utf-16le', errors='ignore')))
    elif r['tag'] == 2206:
        vals = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        print(f"    Kern/Lead: {vals}")
    elif r['tag'] in (4208, 4209):
        val = struct.unpack('<i', r['payload'])[0]
        print(f"    Line Pitch: {val} ({val/500*100}%)")
    elif r['tag'] == 2150:
        w, flag = struct.unpack('<iB', r['payload'])
        print(f"    Col Width: {w} mp ({w/28346.4567:.3f} cm)")
    elif r['tag'] == 2901:
        sz = struct.unpack('<i', r['payload'])[0]
        print(f"    Font Size: {sz} mp ({sz/1000:.1f} pt)")

print("\n--- PAGE 2 NAME STORY (Records 3611 to 3639) ---")
for idx in range(3611, 3640):
    r = doc.records[idx]
    print(f"[{idx}] Tag {r['tag']} (size {r['size']}): {r['payload'].hex()}")
    if r['tag'] == 2201:
        print("    Text:", repr(r['payload'].decode('utf-16le', errors='ignore')))
    elif r['tag'] == 2206:
        vals = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        print(f"    Kern/Lead: {vals}")
    elif r['tag'] in (4208, 4209):
        val = struct.unpack('<i', r['payload'])[0]
        print(f"    Line Pitch: {val} ({val/500*100}%)")
    elif r['tag'] == 2150:
        w, flag = struct.unpack('<iB', r['payload'])
        print(f"    Col Width: {w} mp ({w/28346.4567:.3f} cm)")
    elif r['tag'] == 2901:
        sz = struct.unpack('<i', r['payload'])[0]
        print(f"    Font Size: {sz} mp ({sz/1000:.1f} pt)")
