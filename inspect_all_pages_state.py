from xar_dom_engine import XarDocument
import struct

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)
print(f"Total records in 0_tahap7.xar: {len(doc.records):,}")

# Find all Page tags (Tag 4351 or page boundaries)
page_markers = []
for i, r in enumerate(doc.records):
    if r['tag'] == 4351:
        page_markers.append(i)
print(f"Found {len(page_markers)} page markers: {page_markers}")

# Check Name stories across document
print("\n--- ALL NAME STORIES ---")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'MASRIYAH' in txt:
            # find preceding Tag 2100 & 2150
            p2100 = "NONE"
            p2150 = "NONE"
            for k in range(i, max(0, i-30), -1):
                if doc.records[k]['tag'] == 2100:
                    c = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]["payload"])
                    p2100 = f"coords={c} (X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm)"
                    break
            for k in range(i, max(0, i-30), -1):
                if doc.records[k]['tag'] == 2150:
                    w, fl = struct.unpack('<iB', doc.records[k]["payload"])
                    p2150 = f"width={w} mp ({w/28346.4567:.3f}cm)"
                    break
            print(f"Rec [{i}] Text: {txt!r} | Tag 2100: {p2100} | Tag 2150: {p2150}")

# Check Cabang across document
print("\n--- ALL CABANG OCCURRENCES ---")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'KCP Jakarta Taman Aries' in txt:
            p2100 = "NONE"
            for k in range(i, max(0, i-30), -1):
                if doc.records[k]['tag'] == 2100:
                    c = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]["payload"])
                    p2100 = f"coords={c} (X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm)"
                    break
            print(f"Rec [{i}] Text: {txt!r} | Tag 2100: {p2100}")
