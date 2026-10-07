import struct
from xar_dom_engine import XarDocument

def apply_test():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    # =========================================================================
    # 1. FIX PERIOD DATES (Blank out orphan Tag 2202 '0' or '1' before Period)
    # =========================================================================
    for i, r in enumerate(doc.records):
        if r['tag'] == 2201:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if '01 Jul 2026 - 31 Jul 2026' in txt:
                # Look for preceding Tag 2202 within 10 records
                for j in range(max(0, i-10), i):
                    if doc.records[j]['tag'] == 2202:
                        p_txt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        if p_txt in ('0', '1'):
                            doc.records[j]['payload'] = bytearray(b'\x00\x00')
                            doc.records[j]['size'] = 2
                            print(f"[*] Blanked orphan Period Tag 2202 at [{j}] (was {p_txt!r})")

    # =========================================================================
    # 2. CONFIGURE PAGE 1 NAME STORY
    # =========================================================================
    # Locate Page 1 Name Story (starts around record 964)
    start_p1 = None
    end_p1 = None
    for i in range(940, 980):
        if doc.records[i]['tag'] == 2100:
            coords = struct.unpack(f'<{len(doc.records[i]["payload"])//4}i', doc.records[i]["payload"])
            if len(coords) >= 2 and coords[1] == 736000 and coords[0] in (123000, 123307):
                start_p1 = i
                break

    if start_p1 is not None:
        for j in range(start_p1, start_p1 + 35):
            if doc.records[j]['tag'] == 2203:
                end_p1 = j + 1
                while end_p1 < len(doc.records) and doc.records[end_p1]['tag'] == 0:
                    end_p1 += 1
                break

        print(f"[*] Found Page 1 Name Story from record {start_p1} to {end_p1}")

        # Build clean 2-line Name story for Page 1
        # W = 3.17 cm = 89858 mp, X = 4.350 cm = 123307 mp, Y = 25.964 cm = 736000 mp
        W_317_MP = 89858
        new_name_story_p1 = [
            {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', 123307, 736000, 1))},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', W_317_MP, 1))}, # W = 3.170 cm
            {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
            {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('3e040000')},
            {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')},
            {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('55010000')},
            {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
            {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
            {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
            {'tag': 193,  'size': 0,  'payload': bytearray()},
            {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
            {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% line pitch
            {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% line pitch
            {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # Font size 10000 mp = 8pt
            # Line 1: MASRIYAH MUHAMMAD
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', W_317_MP, 5761, 0))},
            {'tag': 2201, 'size': 36, 'payload': bytearray('MASRIYAH MUHAMMAD '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 2: SAMIAN
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 30961, 5761, -10000))},
            {'tag': 2201, 'size': 14, 'payload': bytearray('SAMIAN '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 3: Trailing / EOP
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10000))},
            {'tag': 2203, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
        ]
        doc.records[start_p1:end_p1] = new_name_story_p1
        print(f"[*] Replaced Page 1 Name Story with 2-line structure (W=3.17cm, 80% leading)")

    # =========================================================================
    # 3. INSERT INDEPENDENT CABANG OBJECT ON PAGE 1
    # =========================================================================
    # Check if Cabang already exists on Page 1 (before Page 2)
    has_cabang_p1 = False
    for i in range(0, 3500):
        if doc.records[i]['tag'] == 2201:
            txt = doc.records[i]['payload'].decode('utf-16le', errors='ignore')
            if 'KCP Jakarta Taman Aries' in txt:
                has_cabang_p1 = True
                print(f"[*] Cabang already exists on Page 1 at record [{i}]")
                break

    if not has_cabang_p1:
        # Find Mandiri Call 14000 on Page 1
        insert_pos_p1 = None
        for i in range(2500, 3500):
            if doc.records[i]['tag'] == 2201:
                txt = doc.records[i]['payload'].decode('utf-16le', errors='ignore')
                if 'Mandiri Call 14000' in txt:
                    for j in range(i, i+10):
                        if doc.records[j]['tag'] == 2203:
                            insert_pos_p1 = j + 1
                            while insert_pos_p1 < len(doc.records) and doc.records[insert_pos_p1]['tag'] == 0:
                                insert_pos_p1 += 1
                            break
                    break

        if insert_pos_p1 is not None:
            # Cabang object: X = 4.378 cm (124,101 mp) or 4.370 cm (123,874 mp), Y = 25.203 cm (714,420 mp)
            # Tag 2100: (124101, 714420, 1)
            cabang_obj_p1 = [
                {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', 124101, 714420, 1))},
                {'tag': 1,    'size': 0,  'payload': bytearray()},
                {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', 0, 0))},
                {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
                {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
                {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80%
                {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')},
                {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('b2010000')},
                {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')},
                {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('55010000')},
                {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
                {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
                {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
                {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
                {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
                {'tag': 193,  'size': 0,  'payload': bytearray()},
                {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
                {'tag': 2200, 'size': 0,  'payload': bytearray()},
                {'tag': 1,    'size': 0,  'payload': bytearray()},
                {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 88118, 5761, 0))},
                {'tag': 2201, 'size': 46, 'payload': bytearray('KCP Jakarta Taman Aries'.encode('utf-16le'))},
                {'tag': 2203, 'size': 0,  'payload': bytearray()},
                {'tag': 0,    'size': 0,  'payload': bytearray()},
                {'tag': 2200, 'size': 0,  'payload': bytearray()},
                {'tag': 1,    'size': 0,  'payload': bytearray()},
                {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10400))},
                {'tag': 2203, 'size': 0,  'payload': bytearray()},
                {'tag': 0,    'size': 0,  'payload': bytearray()},
            ]
            doc.records[insert_pos_p1:insert_pos_p1] = cabang_obj_p1
            print(f"[*] Inserted independent Cabang object on Page 1 at record [{insert_pos_p1}]")

    # =========================================================================
    # 4. SYNC SIZES AND SAVE
    # =========================================================================
    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Page 1 and Page 2 tested & updated! Total records: {len(doc.records):,}")

if __name__ == '__main__':
    apply_test()
