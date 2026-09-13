import struct
from xar_dom_engine import XarDocument

MP_PER_CM = 72000 / 2.54

doc6 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap6.xar')

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

print(f"{'Row':3s} | {'Nom Text T6':15s} | {'Nom MX':8s} | {'Nom KX':8s} | {'Nom Tot (cm)':12s} | {'Sal Text T6':15s} | {'Sal MX':8s} | {'Sal KX':8s} | {'Sal Tot (cm)':12s}")
print("-" * 120)

for row_num, nom_idx, sal_idx in table_master:
    # Nom
    nom_txt = doc6.records[nom_idx]['payload'].decode('utf-16le', errors='replace').strip('\x00')
    nom_mx, nom_kx = 0, 0
    for k in range(max(0, nom_idx - 25), nom_idx):
        if doc6.records[k]['tag'] == 2100:
            nom_mx = struct.unpack('<i', doc6.records[k]['payload'][:4])[0]
            break
    for k in range(max(0, nom_idx - 15), nom_idx):
        if doc6.records[k]['tag'] == 2206:
            nom_kx = struct.unpack('<i', doc6.records[k]['payload'][:4])[0]
            break
            
    # Sal
    sal_txt = doc6.records[sal_idx]['payload'].decode('utf-16le', errors='replace').strip('\x00')
    sal_mx, sal_kx = 0, 0
    for k in range(max(0, sal_idx - 25), sal_idx):
        if doc6.records[k]['tag'] == 2100:
            sal_mx = struct.unpack('<i', doc6.records[k]['payload'][:4])[0]
            break
    for k in range(max(0, sal_idx - 15), sal_idx):
        if doc6.records[k]['tag'] == 2206:
            sal_kx = struct.unpack('<i', doc6.records[k]['payload'][:4])[0]
            break
            
    nom_tot = nom_mx + nom_kx
    sal_tot = sal_mx + sal_kx
    
    print(f"{row_num:3d} | {nom_txt:15s} | {nom_mx:8d} | {nom_kx:8d} | {nom_tot/MP_PER_CM:8.3f} cm | {sal_txt:15s} | {sal_mx:8d} | {sal_kx:8d} | {sal_tot/MP_PER_CM:8.3f} cm")
