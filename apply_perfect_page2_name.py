import struct
from xar_dom_engine import XarDocument

def apply_perfect_page2():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    # Locate Page 2 Name Story:
    # Starts around record 3611 (Tag 2100 with X around 123000, Y=736000)
    # and ends at Tag 0 (record ~3639)
    start_idx = None
    end_idx = None

    for i in range(3550, 3700):
        if doc.records[i]['tag'] == 2100:
            coords = struct.unpack(f'<{len(doc.records[i]["payload"])//4}i', doc.records[i]['payload'])
            if len(coords) >= 2 and coords[1] == 736000 and coords[0] in (123000, 123307, 340000):
                # Check if next text has MASRIYAH
                for j in range(i, i + 30):
                    if doc.records[j]['tag'] == 2201:
                        txt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        if 'MASRIYAH' in txt:
                            start_idx = i
                            break
                if start_idx is not None:
                    break

    # Find the end of this story (the double Tag 0 after Tag 2203)
    for j in range(start_idx, start_idx + 40):
        if doc.records[j]['tag'] == 2203:
            # Story ends after the next two Tag 0s
            end_idx = j + 2
            while end_idx < len(doc.records) and doc.records[end_idx]['tag'] == 0:
                end_idx += 1
            break

    print(f"[*] Found Page 2 Name Story from record {start_idx} to {end_idx}")

    # Build the perfect Page 2 Name Story records
    # W = 3.090 cm = 87591 mp
    # X = 4.350 cm = 123307 mp, Y = 25.964 cm = 736000 mp
    new_story = [
        {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', 123307, 736000, 1))},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', 87591, 1))}, # W = 3.090 cm
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
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 89482, 5761, 0))},
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

    # Replace old story slice with new story slice
    doc.records[start_idx:end_idx] = new_story

    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Page 2 Name Story perfectly replaced! Total records: {len(doc.records):,}")

if __name__ == '__main__':
    apply_perfect_page2()
