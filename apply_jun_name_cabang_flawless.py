import os
import struct
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
p7 = os.path.join(folder, '0_tahap7.xar')

print("=========================================================================")
print("   APPLYING 2-BOX NAME (W=3.17cm, 80% LEADING) & CABANG FOR JUNE")
print(f"   Target: {p7}")
print("=========================================================================\n")

doc = XarDocument(p7)
print(f"[*] Loaded document: {len(doc.records):,} records")

W_317_MP = 89858
X_NAME_MP = 123307
Y_NAME_MP = 736000
X_CABANG_MP = 124101
Y_CABANG_MP = 714420

COLOR_TEXT_JUN = bytearray.fromhex('40040000') # Native Black in June

def make_name_story():
    return [
        {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_NAME_MP, Y_NAME_MP, 1))},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', W_317_MP, 1))},
        {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
        {'tag': 150,  'size': 4,  'payload': COLOR_TEXT_JUN}, # Native Black
        {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')}, # Normal Style
        {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')}, # Font ID 340 (PDF-TTInterphases-Regular)
        {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
        {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
        {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
        {'tag': 193,  'size': 0,  'payload': bytearray()},
        {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
        {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% leading
        {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% leading
        {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
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
        # Line 3: Trailing End Of Paragraph
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
        {'tag': 150,  'size': 4,  'payload': COLOR_TEXT_JUN}, # Native Black
        {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')}, # Normal Style
        {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')}, # Font ID 340 (PDF-TTInterphases-Regular)
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

# 1. Clean Period Date Phantom Blocks across all 7 pages
period_indices = []
for idx_r, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Jun 2026 - 30 Jun 2026' in txt:
            period_indices.append(idx_r)

print(f"[*] Cleaning Period Date Phantom Blocks on {len(period_indices)} pages...")
for p_idx in reversed(period_indices):
    # Ensure text is 01 Jun 2026 - 30 Jun 2026
    doc.records[p_idx]['payload'] = bytearray('01 Jun 2026 - 30 Jun 2026'.encode('utf-16le'))
    doc.records[p_idx]['size'] = len(doc.records[p_idx]['payload'])
    
    start_check = max(0, p_idx - 15)
    for k in range(p_idx - 1, start_check, -1):
        if doc.records[k]['tag'] == 2202:
            t2202_idx = k
            fwd = t2202_idx + 1
            if fwd < p_idx and doc.records[fwd]['tag'] == 1:
                while fwd < p_idx and doc.records[fwd]['tag'] in (1, 4405, 0):
                    fwd += 1
            bwd = t2202_idx
            if doc.records[bwd - 1]['tag'] == 0 and doc.records[bwd - 2]['tag'] == 4405 and doc.records[bwd - 3]['tag'] == 1:
                bwd = bwd - 3
            del doc.records[bwd:fwd]
            break

# 2. Replace Name stories on all 7 pages
name_story_ranges = []
idx_scan = 0
while idx_scan < len(doc.records):
    r = doc.records[idx_scan]
    if r['tag'] == 2100:
        coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
        if len(coords) >= 2 and coords[1] == 736000 and coords[0] in (123000, 123307):
            for j in range(idx_scan, min(len(doc.records), idx_scan+35)):
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
                        name_story_ranges.append((idx_scan, end))
                        idx_scan = end - 1
                        break
    idx_scan += 1

print(f"[*] Replacing Name Story (W=3.17cm, 80% leading) on {len(name_story_ranges)} pages...")
for s, e in reversed(name_story_ranges):
    doc.records[s:e] = make_name_story()

# 3. Insert independent Cabang object after Mandiri Call 14000 on each page
mandiri_ends = []
for idx_m, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'Mandiri Call 14000' in r['payload'].decode('utf-16le', errors='ignore'):
        for j in range(idx_m, min(len(doc.records), idx_m+10)):
            if doc.records[j]['tag'] == 2203:
                end = j + 1
                while end < len(doc.records) and doc.records[end]['tag'] == 0:
                    end += 1
                mandiri_ends.append(end)
                break

print(f"[*] Inserting Independent Cabang Object on {len(mandiri_ends)} pages...")
for m_end in reversed(mandiri_ends):
    has_cabang = False
    for k in range(m_end, min(len(doc.records), m_end + 35)):
        if doc.records[k]['tag'] == 2201 and 'KCP Jakarta Taman Aries' in doc.records[k]['payload'].decode('utf-16le', errors='ignore'):
            has_cabang = True
            break
    if not has_cabang:
        doc.records[m_end:m_end] = make_cabang_obj()

for r in doc.records:
    r['size'] = len(r['payload'])

doc.save(p7)
print(f"\n[SAVED] {os.path.basename(p7)} ({len(doc.records):,} records) [PASS]")
