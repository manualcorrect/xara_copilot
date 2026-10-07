import struct
from xar_dom_engine import XarDocument

def update_width():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Total records: {len(doc.records)}")

    # 3.17 cm = 89858 millipoints
    W_317_MP = round(3.17 * 28346.4566929) # 89858 mp
    print(f"[*] Setting Column Width to {W_317_MP} mp ({W_317_MP/28346.4567:.3f} cm)")

    # Find Tag 2150 in Page 2 Name story (around records 3610-3620)
    found = False
    for i in range(3600, 3630):
        if doc.records[i]['tag'] == 2150:
            doc.records[i]['payload'] = bytearray(struct.pack('<iB', W_317_MP, 1))
            doc.records[i]['size'] = len(doc.records[i]['payload'])
            print(f"[*] Updated Tag 2150 at record [{i}] to W={W_317_MP} mp (3.17 cm)")
            found = True
            break

    if not found:
        print("[ERROR] Tag 2150 not found around record 3610!")
        return

    # Let's also check Line 1 advance width in Tag 2206
    for j in range(3620, 3645):
        if doc.records[j]['tag'] == 2201:
            txt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
            if 'MASRIYAH' in txt:
                kern_idx = j - 1
                if doc.records[kern_idx]['tag'] == 2206:
                    vals = struct.unpack('<iii', doc.records[kern_idx]['payload'])
                    # vals: (width, 5761, 0)
                    doc.records[kern_idx]['payload'] = bytearray(struct.pack('<iii', W_317_MP, vals[1], vals[2]))
                    doc.records[kern_idx]['size'] = 12
                    print(f"[*] Updated Line 1 Kerning at record [{kern_idx}]: W={W_317_MP}")
                break

    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Saved 0_tahap7.xar with W = 3.17 cm!")

if __name__ == '__main__':
    update_width()
