from xar_dom_engine import XarDocument
from verify_exact_widths import glyph_map
import struct

MP_PER_CM = 72000 / 2.54

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

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

TARGET_NOM_RIGHT = 431267 # 15.214 cm
TARGET_SAL_RIGHT = 568306 # 20.049 cm

print("=" * 140)
print(f"{'Row':3s} | {'Nominal Text':15s} | {'Nom W(cm)':9s} | {'Nom MX Old':10s} | {'Nom MX New':10s} | {'Saldo Text':14s} | {'Sal W(cm)':9s} | {'Sal MX Old':10s} | {'Sal MX New':10s}")
print("=" * 140)

for r_num, nom_s, nom_m, nom_l, sal_s, sal_m, sal_l in table_master:
    nom_txt = doc.records[nom_s]['payload'].decode('utf-16le').strip('\x00')
    sal_txt = doc.records[sal_s]['payload'].decode('utf-16le').strip('\x00')
    
    # widths
    w_nom = sum(glyph_map.get(c, 4800) for c in nom_txt)
    w_sal = sum(glyph_map.get(c, 4800) for c in sal_txt)
    
    # current MX
    mx_nom_old = struct.unpack('<i', doc.records[nom_m]['payload'][:4])[0]
    mx_sal_old = struct.unpack('<i', doc.records[sal_m]['payload'][:4])[0]
    
    # new MX
    mx_nom_new = TARGET_NOM_RIGHT - w_nom
    mx_sal_new = TARGET_SAL_RIGHT - w_sal
    
    print(f"{r_num:3d} | {nom_txt:15s} | {w_nom/MP_PER_CM:7.3f} cm | {mx_nom_old/MP_PER_CM:8.3f} cm | {mx_nom_new/MP_PER_CM:8.3f} cm | {sal_txt:14s} | {w_sal/MP_PER_CM:7.3f} cm | {mx_sal_old/MP_PER_CM:8.3f} cm | {mx_sal_new/MP_PER_CM:8.3f} cm")
