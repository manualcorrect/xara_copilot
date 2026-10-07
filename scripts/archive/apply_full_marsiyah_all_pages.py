import struct
from xar_dom_engine import XarDocument

def apply_all_pages():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    W_317_MP = 89858
    X_NAME_MP = 123307
    Y_NAME_MP = 736000
    X_CABANG_MP = 124101
    Y_CABANG_MP = 714420

    def make_name_story():
        return [
            {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_NAME_MP, Y_NAME_MP, 1))},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', W_317_MP, 1))},
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
            {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80%
            {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80%
            {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
            # Line 1
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', W_317_MP, 5761, 0))},
            {'tag': 2201, 'size': 36, 'payload': bytearray('MASRIYAH MUHAMMAD '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 2
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 30961, 5761, -10000))},
            {'tag': 2201, 'size': 14, 'payload': bytearray('SAMIAN '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 3 (Trailing EOP)
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

    # Step 1: Find all Name Stories across document and replace with clean 2-line story
    # We locate all Tag 2100 around Y=736000 and X in (123000, 123307) that lead to MASRIYAH
    name_story_ranges = []
    i = 0
    while i < len(doc.records):
        r = doc.records[i]
        if r['tag'] == 2100:
            coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
            if len(coords) >= 2 and coords[1] == 736000 and coords[0] in (123000, 123307):
                # check if this is a Name story
                for j in range(i, min(len(doc.records), i+35)):
                    if doc.records[j]['tag'] == 2201:
                        txt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        if 'MASRIYAH' in txt:
                            # find end of story (Tag 2203)
                            end = j
                            for k in range(j, min(len(doc.records), j+20)):
                                if doc.records[k]['tag'] == 2203:
                                    end = k + 1
                                    while end < len(doc.records) and doc.records[end]['tag'] == 0:
                                        end += 1
                                    break
                            name_story_ranges.append((i, end))
                            i = end - 1
                            break
        i += 1

    print(f"[*] Found {len(name_story_ranges)} Name stories: {name_story_ranges}")

    # Replace from back to front
    for s, e in reversed(name_story_ranges):
        doc.records[s:e] = make_name_story()
        print(f"[*] Replaced Name story at [{s}..{e}] with clean 2-line structure")

    # Step 2: Ensure every page has independent Cabang object
    # Find all Mandiri Call 14000 positions
    mandiri_ends = []
    for i, r in enumerate(doc.records):
        if r['tag'] == 2201:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if 'Mandiri Call 14000' in txt:
                for j in range(i, min(len(doc.records), i+10)):
                    if doc.records[j]['tag'] == 2203:
                        end = j + 1
                        while end < len(doc.records) and doc.records[end]['tag'] == 0:
                            end += 1
                        mandiri_ends.append(end)
                        break

    print(f"[*] Found {len(mandiri_ends)} Mandiri Call endpoints: {mandiri_ends}")

    # Check which Mandiri Call endpoints already have a Cabang object right after them
    for m_end in reversed(mandiri_ends):
        # Look ahead 30 records to see if Cabang object is already there
        has_cabang = False
        for k in range(m_end, min(len(doc.records), m_end + 35)):
            if doc.records[k]['tag'] == 2201:
                txt = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
                if 'KCP Jakarta Taman Aries' in txt:
                    has_cabang = True
                    break
        if not has_cabang:
            print(f"[*] Inserting Cabang object after Mandiri Call at index [{m_end}]")
            doc.records[m_end:m_end] = make_cabang_obj()
        else:
            print(f"[*] Mandiri Call at [{m_end}] already followed by Cabang object")

    # Sync sizes and save
    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Replicated clean Name & Cabang structure across all 8 pages! Total records: {len(doc.records):,}")

if __name__ == '__main__':
    apply_all_pages()
