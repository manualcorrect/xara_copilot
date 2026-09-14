import os
import struct
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== INSPECTING HEADERS & TEXT OBJECTS ACROSS ALL 10 PAGES IN AUG/0.XAR ===")
page_num = 0
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if any(w in txt for w in ['MASRIYAH', 'Mandiri Call', 'KCP', 'Cabang', 'Jl.', 'RT.', 'RW.', 'Periode', 'Dicetak', 'Halaman', 'Page', 'No. Rekening', 'Account No']):
            f_id = None
            c_id = None
            pos = None
            w_box = None
            t2206_val = None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 2907:
                    f_id = doc.records[k]['payload'].hex()
                if doc.records[k]['tag'] == 150:
                    c_id = doc.records[k]['payload'].hex()
                if doc.records[k]['tag'] == 2100:
                    pos = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]["payload"])
                if doc.records[k]['tag'] == 2150:
                    w_box = struct.unpack('<iB', doc.records[k]['payload'])
                if doc.records[k]['tag'] == 2206:
                    t2206_val = struct.unpack('<iii', doc.records[k]['payload'][:12])
            print(f'Rec {i:5d}: {txt!r:35s} | Font: {f_id} | Col: {c_id} | Pos: {pos} | Box: {w_box} | T2206: {t2206_val}')
