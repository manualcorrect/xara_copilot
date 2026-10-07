from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

print("=" * 80)
print("INSPECTING NOMINAL TAG 2100 AND TAG 2206 ACROSS ALL ROWS IN 0.xar")
print("=" * 80)

for i in range(len(doc0.records)):
    r = doc0.records[i]
    if r['tag'] == 2206 and i + 1 < len(doc0.records):
        r_txt = doc0.records[i+1]
        if r_txt['tag'] in (2201, 2202):
            txt = r_txt['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
            if (txt.startswith('-') or txt.startswith('+')) and ',' in txt:
                adv = struct.unpack('<iii', r['payload'][:12])
                
                # find parent tag 2100 before rec i
                mat = None
                mat_rec = None
                for k in range(max(0, i-25), i):
                    if doc0.records[k]['tag'] == 2100:
                        mat = struct.unpack('<iii', doc0.records[k]['payload'][:12])
                        mat_rec = k
                
                mat_x = mat[0] if mat else 0
                mat_x_cm = mat_x * 2.54 / 72000
                print(f"Nominal Rec {i+1:5d}: '{txt:18s}' | Tag 2100 Rec {mat_rec:5d}: mp={mat_x:6d} ({mat_x_cm:.4f}cm) | Tag 2206 Rec {i:5d}: adv={adv[0]:5d}")
