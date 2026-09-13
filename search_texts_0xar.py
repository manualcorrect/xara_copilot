from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

print("=" * 80)
print("SEARCHING TEXT RECORDS IN 0.xar")
print("=" * 80)

count = 0
for i, rec in enumerate(doc0.records):
    if rec['tag'] in (2201, 2202):
        txt = rec['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if ',' in txt and any(c.isdigit() for c in txt):
            # find preceding tag 2100
            mat_info = ""
            mat_rec = None
            for k in range(max(0, i-30), i):
                if doc0.records[k]['tag'] == 2100:
                    mat = struct.unpack('<iii', doc0.records[k]['payload'][:12])
                    x_cm = mat[0] * 2.54 / 72000
                    y_cm = mat[1] * 2.54 / 72000
                    mat_info = f"Tag 2100 Rec {k:5d}: X={x_cm:.4f}cm (mp={mat[0]}), Y={y_cm:.4f}cm"
                    mat_rec = k
            print(f"Rec {i:5d} [Tag {rec['tag']}]: '{txt:18s}' | {mat_info}")
            count += 1
            if count >= 40:
                break
