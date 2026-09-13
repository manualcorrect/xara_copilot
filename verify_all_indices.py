from xar_dom_engine import XarDocument
from verify_exact_widths import glyph_map
import struct

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

print("=== VERIFY RECORD TAGS AND PAYLOADS ACROSS ALL 17 ROWS ===")
all_valid = True
for r_num, nom_s, nom_m, nom_l, sal_s, sal_m, sal_l in table_master:
    # Check Nominal
    tag_nm = doc.records[nom_m]['tag']
    tag_nl = doc.records[nom_l]['tag']
    tag_ns = doc.records[nom_s]['tag']
    
    # Check Saldo
    tag_sm = doc.records[sal_m]['tag']
    tag_sl = doc.records[sal_l]['tag']
    tag_ss = doc.records[sal_s]['tag']
    
    ok = (tag_nm == 2100 and tag_nl == 2206 and tag_ns == 2201 and
          tag_sm == 2100 and tag_sl == 2206 and tag_ss == 2201)
    if not ok:
        print(f"Row {r_num:2d} MISMATCH: nom=({tag_nm}, {tag_nl}, {tag_ns}), sal=({tag_sm}, {tag_sl}, {tag_ss})")
        all_valid = False
    else:
        # print sizes
        len_nm = len(doc.records[nom_m]['payload'])
        len_nl = len(doc.records[nom_l]['payload'])
        len_sm = len(doc.records[sal_m]['payload'])
        len_sl = len(doc.records[sal_l]['payload'])
        print(f"Row {r_num:2d} OK: Nom(Mat={nom_m}[{len_nm}b], Line={nom_l}[{len_nl}b]), Sal(Mat={sal_m}[{len_sm}b], Line={sal_l}[{len_sl}b])")

print(f"\nALL RECORDS VALID: {all_valid}")
