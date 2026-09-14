import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== PAGE 5 NAME STORY ===")
for j in range(11830, 11880):
    if j >= len(doc.records):
        break
    rec = doc.records[j]
    hex_p = rec['payload'].hex()
    info = ""
    if rec['tag'] == 2201:
        info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
    elif rec['tag'] == 2150:
        w, flag = struct.unpack('<iB', rec['payload'])
        info = f" | col width: {w} mp ({w/28346.4567:.3f} cm), flag: {flag}"
    elif rec['tag'] == 2100:
        coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
    elif rec['tag'] == 2206:
        vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | kern/lead: {vals}"
    elif rec['tag'] == 2901:
        size = struct.unpack('<i', rec['payload'])[0]
        info = f" | font size: {size} mp ({size/1000:.1f}pt)"
    elif rec['tag'] in (4208, 4209):
        val = struct.unpack('<i', rec['payload'])[0]
        info = f" | line pitch: {val} ({val/500*100:.1f}%)"
    print(f"[{j}] Tag {rec['tag']} (len {rec['size']}): {hex_p}{info}")

print("\n=== PAGE 2 NAME STORY ===")
for j in range(3605, 3655):
    if j >= len(doc.records):
        break
    rec = doc.records[j]
    hex_p = rec['payload'].hex()
    info = ""
    if rec['tag'] == 2201:
        info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
    elif rec['tag'] == 2150:
        w, flag = struct.unpack('<iB', rec['payload'])
        info = f" | col width: {w} mp ({w/28346.4567:.3f} cm), flag: {flag}"
    elif rec['tag'] == 2100:
        coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
    elif rec['tag'] == 2206:
        vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | kern/lead: {vals}"
    elif rec['tag'] == 2901:
        size = struct.unpack('<i', rec['payload'])[0]
        info = f" | font size: {size} mp ({size/1000:.1f}pt)"
    elif rec['tag'] in (4208, 4209):
        val = struct.unpack('<i', rec['payload'])[0]
        info = f" | line pitch: {val} ({val/500*100:.1f}%)"
    print(f"[{j}] Tag {rec['tag']} (len {rec['size']}): {hex_p}{info}")
