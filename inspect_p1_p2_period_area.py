import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== PAGE 1 PERIOD AREA (Records 1000 to 1035) ===")
for idx in range(1000, 1035):
    rec = doc.records[idx]
    info = ""
    if rec['tag'] in (2201, 2202):
        info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
    elif rec['tag'] == 2100:
        coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
    elif rec['tag'] == 2206:
        vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | kern/lead: {vals}"
    print(f"[{idx}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()[:30]}{info}")

print("\n=== PAGE 2 PERIOD AREA (Records 3660 to 3690) ===")
for idx in range(3660, 3690):
    rec = doc.records[idx]
    info = ""
    if rec['tag'] in (2201, 2202):
        info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
    elif rec['tag'] == 2100:
        coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
    elif rec['tag'] == 2206:
        vals = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
        info = f" | kern/lead: {vals}"
    print(f"[{idx}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()[:30]}{info}")
