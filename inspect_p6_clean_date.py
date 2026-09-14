from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar')

print("=== INSPECTING PAGE 6 CLEAN DATE STORY ===")
for j in range(14710, 14745):
    r = doc.records[j]
    txt = r['payload'].decode('utf-16le', errors='ignore') if r['tag'] in (2201, 2202) else ''
    coords = ''
    if r['tag'] == 2100:
        c = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        coords = f' coords={c} (X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm)'
    elif r['tag'] == 2206:
        vals = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        coords = f' kern/lead={vals}'
    print(f"[{j}] Tag {r['tag']} (sz {r['size']}): {txt!r}{coords}")
