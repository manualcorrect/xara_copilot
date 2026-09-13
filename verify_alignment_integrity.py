from xar_dom_engine import XarDocument
import struct

MP_PER_CM = 72000 / 2.54

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

print("=== VERIFICATION AFTER RIGHT-ALIGNMENT ===")
print(f"Total Records: {len(doc.records)}")

# Check Font definition records 0-1100
font_tags = [doc.records[i]['tag'] for i in range(1100)]
print(f"Records 0-1100 tag count: {len(font_tags)}, has 2000: {2000 in font_tags}, has 4350: {4350 in font_tags}")

# Check Table Rows
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

for r_num, nom_s, nom_m, nom_l, sal_s, sal_m, sal_l in table_master:
    nom_txt = doc.records[nom_s]['payload'].decode('utf-16le').strip('\x00')
    sal_txt = doc.records[sal_s]['payload'].decode('utf-16le').strip('\x00')
    
    nm_x = struct.unpack('<i', doc.records[nom_m]['payload'][:4])[0]
    nl_w = struct.unpack('<i', doc.records[nom_l]['payload'][:4])[0]
    
    sm_x = struct.unpack('<i', doc.records[sal_m]['payload'][:4])[0]
    sl_w = struct.unpack('<i', doc.records[sal_l]['payload'][:4])[0]
    
    nom_r = nm_x + nl_w
    sal_r = sm_x + sl_w
    
    # Check color
    nom_col = ""
    for k in range(max(0, nom_s - 25), nom_s):
        if doc.records[k]['tag'] == 150:
            nom_col = doc.records[k]['payload'].hex()
            break
            
    print(f"Row {r_num:2d} | Nom: {nom_txt:14s} (Left={nm_x/MP_PER_CM:6.3f} cm, Right={nom_r/MP_PER_CM:6.3f} cm, Col={nom_col}) | Sal: {sal_txt:13s} (Left={sm_x/MP_PER_CM:6.3f} cm, Right={sal_r/MP_PER_CM:6.3f} cm)")

