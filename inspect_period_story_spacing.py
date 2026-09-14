import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== DETAILED INSPECTION OF PERIOD STORIES (PAGE 1 & 2) ===")

def inspect_range(start, end, label):
    print(f"\n--- {label} (records {start}..{end}) ---")
    for i in range(start, end):
        r = doc.records[i]
        info = ""
        if r['tag'] in (2201, 2202):
            info = " | text: " + repr(r['payload'].decode('utf-16le', errors='ignore'))
        elif r['tag'] == 2100:
            coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
            info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
        elif r['tag'] == 2150:
            w, flag = struct.unpack('<iB', r['payload'])
            info = f" | col width: {w} mp ({w/28346.4567:.3f}cm)"
        elif r['tag'] == 2206:
            vals = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
            info = f" | kern/lead: {vals}"
        elif r['tag'] == 2204:
            vals = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
            info = f" | tag 2204: {vals}"
        elif r['tag'] == 4204:
            info = f" | tag 4204: hex={r['payload'].hex()}"
        print(f"[{i}] Tag {r['tag']} (sz {r['size']}): {r['payload'].hex()}{info}")

# Page 1 Period Story is around record 995 to 1040
inspect_range(995, 1040, "PAGE 1 PERIOD STORY")

# Page 2 Period Story is around record 3675 to 3725
inspect_range(3675, 3725, "PAGE 2 PERIOD STORY")
