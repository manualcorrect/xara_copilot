import os
import struct
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
p0 = os.path.join(folder, '0.xar')
p7 = os.path.join(folder, '0_tahap7.xar')

doc0 = XarDocument(p0)
print(f"=== JUN 0.XAR ({len(doc0.records):,} records) ===")

pages = []
for i, r in enumerate(doc0.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if any(w in txt for w in ['ROY DARWIN', 'MASRIYAH', 'Mandiri Call', 'KCP']):
            pos = None
            w_box = None
            font_id = None
            col = None
            t6 = None
            for k in range(max(0, i-25), i):
                if doc0.records[k]['tag'] == 2100:
                    pos = struct.unpack(f'<{len(doc0.records[k]["payload"])//4}i', doc0.records[k]["payload"])
                if doc0.records[k]['tag'] == 2150:
                    w_box = struct.unpack('<iB', doc0.records[k]['payload'])
                if doc0.records[k]['tag'] == 2907:
                    font_id = doc0.records[k]['payload'].hex()
                if doc0.records[k]['tag'] == 150:
                    col = doc0.records[k]['payload'].hex()
                if doc0.records[k]['tag'] == 2206:
                    t6 = struct.unpack('<iii', doc0.records[k]['payload'][:12])
            print(f"Rec {i:5d}: {txt!r:30s} | Pos: {pos} | Box: {w_box} | Font: {font_id} | Col: {col} | T2206: {t6}")

if os.path.exists(p7):
    doc7 = XarDocument(p7)
    print(f"\n=== JUN 0_TAHAP7.XAR ({len(doc7.records):,} records) ===")
    for i, r in enumerate(doc7.records):
        if r['tag'] == 2201:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if any(w in txt for w in ['MASRIYAH', 'SAMIAN', 'KCP Jakarta Taman Aries']):
                pos = None
                w_box = None
                font_id = None
                col = None
                t6 = None
                for k in range(max(0, i-25), i):
                    if doc7.records[k]['tag'] == 2100:
                        pos = struct.unpack(f'<{len(doc7.records[k]["payload"])//4}i', doc7.records[k]["payload"])
                    if doc7.records[k]['tag'] == 2150:
                        w_box = struct.unpack('<iB', doc7.records[k]['payload'])
                    if doc7.records[k]['tag'] == 2907:
                        font_id = doc7.records[k]['payload'].hex()
                    if doc7.records[k]['tag'] == 150:
                        col = doc7.records[k]['payload'].hex()
                    if doc7.records[k]['tag'] == 2206:
                        t6 = struct.unpack('<iii', doc7.records[k]['payload'][:12])
                print(f"Rec {i:5d}: {txt!r:30s} | Pos: {pos} | Box: {w_box} | Font: {font_id} | Col: {col} | T2206: {t6}")
