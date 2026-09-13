from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

table_master = [
    (1, 1565, 1544),
    (2, 1756, 1711),
    (3, 2016, 1958),
    (4, 2189, 2154),
    (5, 2352, 2331),
    (6, 2495, 2442),
    (7, 2657, 2631),
    (8, 2842, 2811),
    (9, 2944, 2923),
    (10, 3051, 3030),
    (11, 4425, 4381),
    (12, 4549, 4505),
    (13, 4767, 4706),
    (14, 4983, 4948),
    (15, 6405, 6361),
    (16, 6598, 6554),
    (17, 6740, 6719)
]

print("CURRENT TEXT IN TAHAP 7:")
for row_num, nom_idx, sal_idx in table_master:
    nom_txt = doc.records[nom_idx]['payload'].decode('utf-16le', errors='replace').strip('\x00')
    sal_txt = doc.records[sal_idx]['payload'].decode('utf-16le', errors='replace').strip('\x00')
    print(f"Row {row_num:2d} | Nominal: '{nom_txt:15s}' | Saldo: '{sal_txt:15s}'")
