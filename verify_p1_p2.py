import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== PAGE 1 VERIFICATION ===")
for i in range(950, 1030):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        print(f"[{i}] Tag {r['tag']}: {repr(r['payload'].decode('utf-16le', errors='ignore'))}")
    elif r['tag'] == 2150:
        w, flag = struct.unpack('<iB', r['payload'])
        print(f"[{i}] Tag 2150: Col Width = {w} mp ({w/28346.4567:.3f} cm)")
    elif r['tag'] in (4208, 4209):
        val = struct.unpack('<i', r['payload'])[0]
        print(f"[{i}] Tag {r['tag']}: Line Pitch = {val} ({val/500*100}%)")

print("\n=== PAGE 1 CABANG OBJECT ===")
for i in range(3090, 3140):
    r = doc.records[i]
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'KCP' in txt:
            # find preceding Tag 2100
            for k in range(i, max(0, i-25), -1):
                if doc.records[k]['tag'] == 2100:
                    coords = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]["payload"])
                    print(f"[{i}] Cabang Text: {txt!r}, Coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)")
                    break

print("\n=== PAGE 2 VERIFICATION ===")
for i in range(3630, 3715):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if txt:
            print(f"[{i}] Tag {r['tag']}: {txt!r}")
    elif r['tag'] == 2150:
        w, flag = struct.unpack('<iB', r['payload'])
        print(f"[{i}] Tag 2150: Col Width = {w} mp ({w/28346.4567:.3f} cm)")

print("\n=== ALL PERIOD DATES CHECK ===")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Jul 2026' in txt and ('01' in txt or '31' in txt or '-' in txt):
            # check previous tag 2202
            t2202_info = "NONE"
            for k in range(max(0, i-10), i):
                if doc.records[k]['tag'] == 2202:
                    t2202_info = repr(doc.records[k]['payload'].decode('utf-16le', errors='ignore'))
            print(f"Period at [{i}]: {txt!r} | Preceding Tag 2202: {t2202_info}")
