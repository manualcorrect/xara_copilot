import struct
from xar_dom_engine import XarDocument

def apply_name_column_styling_page2():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    # Target: Page 2 Nama Story
    # 1. Update Tag 2100 Matrix X = 4.350 cm (123,307 mp), Y = 25.964 cm (736,000 mp)
    X_435_MP = 123307 # 4.350 cm
    Y_PAGE2_MP = 736000 # 25.964 cm
    doc.records[3611]['payload'] = bytearray(struct.pack('<iii', X_435_MP, Y_PAGE2_MP, 1))
    doc.records[3611]['size'] = 12

    # 2. Update Tag 2150 Column Width = 3.090 cm (87,591 mp)
    W_309_MP = 87591 # 3.090 cm
    doc.records[3613]['payload'] = bytearray(struct.pack('<iB', W_309_MP, 1))
    doc.records[3613]['size'] = 5

    # 3. Add / Update Tag 4208 & Tag 4209 for 80% Proportional Line Spacing
    # Check if Tag 4208 and 4209 exist before Tag 2200 at Rec 3626
    # In Page 2, let's insert Tag 4208 (400 = 80%) & Tag 4209 (400 = 80%)
    # Let's inspect records between 3614 and 3626
    has_t4208 = False
    for r in range(3614, 3626):
        if doc.records[r]['tag'] == 4208:
            doc.records[r]['payload'] = bytearray.fromhex('90010000') # 400 = 80%
            doc.records[r]['size'] = 4
            has_t4208 = True
        elif doc.records[r]['tag'] == 4209:
            doc.records[r]['payload'] = bytearray.fromhex('90010000')
            doc.records[r]['size'] = 4

    if not has_t4208:
        # Insert Tag 4208 and Tag 4209 before Tag 2200 (at Rec 3626)
        doc.records.insert(3626, {'tag': 4209, 'size': 4, 'payload': bytearray.fromhex('90010000')})
        doc.records.insert(3626, {'tag': 4208, 'size': 4, 'payload': bytearray.fromhex('90010000')})

    # Find the updated index of Tag 2206 for Line 1 & Line 2
    for r in range(3620, 3645):
        if doc.records[r]['tag'] == 2201:
            txt = doc.records[r]['payload'].decode('utf-16le', errors='ignore')
            if 'MASRIYAH' in txt:
                # Line 1 advance width
                kern_r1 = r - 1
                doc.records[kern_r1]['payload'] = bytearray.fromhex('8a5d01008116000000000000') # w=89482 mp, dy=0
                doc.records[kern_r1]['size'] = 12
            elif 'SAMIAN' in txt:
                # Line 2 kerning / leading (80% leading = -10,000 mp)
                kern_r2 = r - 1
                doc.records[kern_r2]['payload'] = bytearray.fromhex('f178000081160000f0d8ffff') # w=30961 mp, dy=-10000 mp
                doc.records[kern_r2]['size'] = 12

    # 4. Sync sizes and save
    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Applied W=3.09cm, 80% line spacing, X=4.35cm on Page 2!")
    print(f"[*] Total records: {len(doc.records):,}")

if __name__ == '__main__':
    apply_name_column_styling_page2()
