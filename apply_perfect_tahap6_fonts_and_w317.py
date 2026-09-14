import struct
from xar_dom_engine import XarDocument

def apply_fix():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    W_317_MP = 89858 # 3.17 cm
    X_NAME_MP = 123307 # 4.350 cm
    Y_NAME_MP = 736000 # 25.964 cm
    X_CABANG_MP = 124101 # 4.378 cm
    Y_CABANG_MP = 714420 # 25.203 cm

    # Exact Tahap 6 / Native 0.xar Font and Color tags:
    # Tag 2907: Font ID 340 = 54010000 (PDF-TTInterphases-Regular)
    # Tag 2906: Style = 401f0000
    # Tag 150:  Color = 3d040000 (Native Black)
    # Tag 2901: Size = 10000 mp (8pt) = 10270000
    # Tag 4208: Pitch = 400 (80%) = 90010000
    # Tag 4209: Pitch = 400 (80%) = 90010000

    def make_name_story():
        return [
            {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_NAME_MP, Y_NAME_MP, 1))},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', W_317_MP, 1))}, # W = 3.17 cm
            {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
            {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('3d040000')}, # Native Black (Tahap 6)
            {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')}, # Native Style
            {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')}, # Font ID 340 (PDF-TTInterphases-Regular)
            {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
            {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
            {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
            {'tag': 193,  'size': 0,  'payload': bytearray()},
            {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('52010000')},
            {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% line pitch
            {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% line pitch
            {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt font size
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
            # Line 3: Trailing EOP
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10000))},
            {'tag': 2203, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
        ]

    def make_cabang_obj():
        return [
            {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_CABANG_MP, Y_CABANG_MP, 1))},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', 0, 0))},
            {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
            {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('3d040000')}, # Native Black (Tahap 6)
            {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')}, # Native Style
            {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')}, # Font ID 340 (PDF-TTInterphases-Regular)
            {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
            {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
            {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
            {'tag': 193,  'size': 0,  'payload': bytearray()},
            {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('52010000')},
            {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% line pitch
            {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% line pitch
            {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt font size
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

    # Find and update all Name stories across document
    name_ranges = []
    i = 0
    while i < len(doc.records):
        r = doc.records[i]
        if r['tag'] == 2100:
            coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
            if len(coords) >= 2 and coords[1] == 736000 and coords[0] in (123000, 123307):
                for j in range(i, min(len(doc.records), i+35)):
                    if doc.records[j]['tag'] == 2201:
                        txt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        if 'MASRIYAH' in txt:
                            end = j
                            for k in range(j, min(len(doc.records), j+20)):
                                if doc.records[k]['tag'] == 2203:
                                    end = k + 1
                                    while end < len(doc.records) and doc.records[end]['tag'] == 0:
                                        end += 1
                                    break
                            name_ranges.append((i, end))
                            i = end - 1
                            break
        i += 1

    print(f"[*] Found {len(name_ranges)} Name stories: {name_ranges}")
    for s, e in reversed(name_ranges):
        doc.records[s:e] = make_name_story()
        print(f"[*] Updated Name story at [{s}..{e}] with Font ID 340 & W=3.17cm")

    # Find and update all Cabang objects across document
    cabang_ranges = []
    i = 0
    while i < len(doc.records):
        r = doc.records[i]
        if r['tag'] == 2100:
            coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
            if len(coords) >= 2 and coords[0] == X_CABANG_MP and coords[1] == Y_CABANG_MP:
                for j in range(i, min(len(doc.records), i+35)):
                    if doc.records[j]['tag'] == 2201:
                        txt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        if 'KCP Jakarta Taman Aries' in txt:
                            end = j
                            for k in range(j, min(len(doc.records), j+15)):
                                if doc.records[k]['tag'] == 2203:
                                    end = k + 1
                                    while end < len(doc.records) and doc.records[end]['tag'] == 0:
                                        end += 1
                                    break
                            cabang_ranges.append((i, end))
                            i = end - 1
                            break
        i += 1

    print(f"[*] Found {len(cabang_ranges)} Cabang objects: {cabang_ranges}")
    for s, e in reversed(cabang_ranges):
        doc.records[s:e] = make_cabang_obj()
        print(f"[*] Updated Cabang object at [{s}..{e}] with Font ID 340 & Black Color")

    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Applied perfect Tahap 6 Font (ID 340) & W=3.17cm across all 8 pages! Total records: {len(doc.records):,}")

if __name__ == '__main__':
    apply_fix()
