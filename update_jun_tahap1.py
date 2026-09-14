import os
import struct
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
p1 = os.path.join(folder, '0_tahap1.xar')

doc = XarDocument(p1)
W_317_MP = 89858
X_NAME_MP = 123307
Y_NAME_MP = 736000
COLOR_TEXT_JUN = bytearray.fromhex('40040000')

def make_name_story():
    return [
        {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_NAME_MP, Y_NAME_MP, 1))},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', W_317_MP, 1))},
        {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
        {'tag': 150,  'size': 4,  'payload': COLOR_TEXT_JUN},
        {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')},
        {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')},
        {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
        {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
        {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
        {'tag': 193,  'size': 0,  'payload': bytearray()},
        {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
        {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')},
        {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')},
        {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')},
        {'tag': 2200, 'size': 0,  'payload': bytearray()},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', W_317_MP, 5761, 0))},
        {'tag': 2201, 'size': 36, 'payload': bytearray('MASRIYAH MUHAMMAD '.encode('utf-16le'))},
        {'tag': 4211, 'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
        {'tag': 2200, 'size': 0,  'payload': bytearray()},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 30961, 5761, -10000))},
        {'tag': 2201, 'size': 14, 'payload': bytearray('SAMIAN '.encode('utf-16le'))},
        {'tag': 4211, 'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
        {'tag': 2200, 'size': 0,  'payload': bytearray()},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10000))},
        {'tag': 2203, 'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
    ]

# Replace Name stories on all 7 pages
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

for s, e in reversed(name_story_ranges):
    doc.records[s:e] = make_name_story()

for r in doc.records:
    r['size'] = len(r['payload'])

doc.save(p1)
print(f"[SAVED] 0_tahap1.xar ({len(doc.records):,} records)")
