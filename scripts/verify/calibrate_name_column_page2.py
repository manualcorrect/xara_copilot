import struct
from xar_dom_engine import XarDocument

def calibrate_page2_name():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    # 1. Update Tag 2100 Matrix X = 4.350 cm (123,307 mp), Y = 25.964 cm (736,000 mp)
    X_435_MP = 123307 # 4.350 cm
    Y_PAGE2_MP = 736000 # 25.964 cm
    doc.records[3611]['payload'] = bytearray(struct.pack('<iii', X_435_MP, Y_PAGE2_MP, 1))
    doc.records[3611]['size'] = 12

    # 2. Update Tag 2150 Column Width = 3.090 cm (87,591 mp)
    W_309_MP = 87591 # 3.090 cm
    doc.records[3613]['payload'] = bytearray(struct.pack('<iB', W_309_MP, 1))
    doc.records[3613]['size'] = 5

    # 3. Update Tag 2901 Font Size to 8pt / 10,000 mp (10270000)
    doc.records[3617]['payload'] = bytearray.fromhex('10270000')
    doc.records[3617]['size'] = 4

    # 4. Set Proportional Line Spacing to 80% (Tag 4208 = 400, Tag 4209 = 400)
    doc.records[3626]['payload'] = bytearray.fromhex('90010000') # 400 = 80%
    doc.records[3626]['size'] = 4
    doc.records[3627]['payload'] = bytearray.fromhex('90010000')
    doc.records[3627]['size'] = 4

    # 5. Set Line 1 Kerning (Advance Width = 3.09cm, dy = 0)
    doc.records[3630]['payload'] = bytearray(struct.pack('<iii', W_309_MP, 5761, 0))
    doc.records[3630]['size'] = 12

    # 6. Set Line 2 Kerning (80% leading = -8,000 mp)
    doc.records[3635]['payload'] = bytearray(struct.pack('<iii', 30961, 5761, -8000))
    doc.records[3635]['size'] = 12

    # 7. Sync record sizes and save
    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Page 2 Name column calibrated: W=3.09cm, Line Spacing=80%, Font=8pt, X=4.35cm!")

if __name__ == '__main__':
    calibrate_page2_name()
