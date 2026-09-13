import struct
from xar_dom_engine import XarDocument
from verify_exact_widths import glyph_map

MP_PER_CM = 72000 / 2.54 # 28346.4567

TARGET_NOM_RIGHT = 431267  # 15.214 cm (Row 1 Nominal Right Edge)
TARGET_SAL_RIGHT = 568306  # 20.049 cm (Row 1 Saldo Right Edge)

table_master = [
    (1, 1565, 1548, 1564, 1544, 1527, 1543),
    (2, 1756, 1739, 1755, 1711, 1695, 1710),
    (3, 2016, 1999, 2015, 1958, 1942, 1957),
    (4, 2189, 2172, 2188, 2154, 2138, 2153),
    (5, 2352, 2335, 2351, 2331, 2314, 2330),
    (6, 2495, 2478, 2494, 2442, 2426, 2441),
    (7, 2657, 2640, 2656, 2631, 2614, 2630),
    (8, 2842, 2825, 2841, 2811, 2794, 2810),
    (9, 2944, 2927, 2943, 2923, 2906, 2922),
    (10, 3051, 3034, 3050, 3030, 3013, 3029),
    (11, 4425, 4408, 4424, 4381, 4365, 4380),
    (12, 4549, 4532, 4548, 4505, 4489, 4504),
    (13, 4767, 4750, 4766, 4706, 4690, 4705),
    (14, 4983, 4966, 4982, 4948, 4932, 4947),
    (15, 6405, 6388, 6404, 6361, 6345, 6360),
    (16, 6598, 6581, 6597, 6554, 6538, 6553),
    (17, 6740, 6723, 6739, 6719, 6702, 6718)
]

def update_row_alignment(file_path):
    doc = XarDocument(file_path)
    print(f"Loaded: {file_path} ({len(doc.records)} records)")
    
    print("\n" + "=" * 135)
    print(f"{'Row':3s} | {'Nominal Text':15s} | {'Nom Left(cm)':12s} | {'Nom Right(cm)':13s} | {'Saldo Text':14s} | {'Sal Left(cm)':12s} | {'Sal Right(cm)':13s}")
    print("=" * 135)
    
    for r_num, nom_s, nom_m, nom_l, sal_s, sal_m, sal_l in table_master:
        # 1. Nominal
        nom_txt = doc.records[nom_s]['payload'].decode('utf-16le').strip('\x00')
        w_nom = sum(glyph_map.get(c, 4800) for c in nom_txt)
        
        # We align all rows so that right edge matches TARGET_NOM_RIGHT
        mx_nom_new = TARGET_NOM_RIGHT - w_nom
        
        # Update Tag 2100 (Matrix)
        p_m = doc.records[nom_m]['payload']
        x, y, flags = struct.unpack('<iii', p_m[:12])
        doc.records[nom_m]['payload'] = bytearray(struct.pack('<iii', mx_nom_new, y, flags))
        doc.records[nom_m]['size'] = len(doc.records[nom_m]['payload'])
        
        # Update Tag 2206 (Line Advance Width)
        p_l = doc.records[nom_l]['payload']
        w, h, flags_l = struct.unpack('<iii', p_l[:12])
        doc.records[nom_l]['payload'] = bytearray(struct.pack('<iii', w_nom, h, flags_l))
        doc.records[nom_l]['size'] = len(doc.records[nom_l]['payload'])
        
        nom_right = mx_nom_new + w_nom
        
        # 2. Saldo
        sal_txt = doc.records[sal_s]['payload'].decode('utf-16le').strip('\x00')
        w_sal = sum(glyph_map.get(c, 4800) for c in sal_txt)
        
        # We align all rows so that right edge matches TARGET_SAL_RIGHT
        mx_sal_new = TARGET_SAL_RIGHT - w_sal
        
        # Update Tag 2100 (Matrix)
        p_sm = doc.records[sal_m]['payload']
        sx, sy, sflags = struct.unpack('<iii', p_sm[:12])
        doc.records[sal_m]['payload'] = bytearray(struct.pack('<iii', mx_sal_new, sy, sflags))
        doc.records[sal_m]['size'] = len(doc.records[sal_m]['payload'])
        
        # Update Tag 2206 (Line Advance Width)
        p_sl = doc.records[sal_l]['payload']
        sw, sh, sflags_l = struct.unpack('<iii', p_sl[:12])
        doc.records[sal_l]['payload'] = bytearray(struct.pack('<iii', w_sal, sh, sflags_l))
        doc.records[sal_l]['size'] = len(doc.records[sal_l]['payload'])
        
        sal_right = mx_sal_new + w_sal
        
        print(f"{r_num:3d} | {nom_txt:15s} | {mx_nom_new/MP_PER_CM:10.3f} cm | {nom_right/MP_PER_CM:11.3f} cm | {sal_txt:14s} | {mx_sal_new/MP_PER_CM:10.3f} cm | {sal_right/MP_PER_CM:11.3f} cm")

    # Save changes
    doc.save(file_path)
    print("\n[SUCCESS] Document saved with updated right-alignment coordinates!")

if __name__ == "__main__":
    target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar'
    update_row_alignment(target_file)
