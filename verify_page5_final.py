from xar_dom_engine import XarDocument
import struct

doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar')

print("=" * 100)
print("FINAL VERIFICATION: PAGE 5 (ROWS 50 to 58)")
print("=" * 100)

rows_to_check = [
    (50, 12626, 12749, 12648, 12722, 12689, 12683),
    (51, 12771, 12904, 12793, 12877, 12844, 12838),
    (52, 12926, 13049, 12948, 13027, 12994, 12988),
    (53, 13071, 13194, 13093, 13167, 13134, 13128),
    (54, 13216, 13347, 13238, 13320, 13287, 13281),
    (55, 13374, 13497, 13396, 13470, 13437, 13431),
    (56, 13519, 13642, 13541, 13620, 13587, 13581),
    (57, 13664, 13799, 13686, 13772, 13739, 13733),
    (58, 13821, 13949, 13843, 13922, 13889, 13883),
]

for r_no, d_rec, t_rec, u_rec, nom_rec, sal_rec, k_rec in rows_to_check:
    d_txt = doc7.records[d_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    t_txt = doc7.records[t_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    u_txt = doc7.records[u_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    nom_txt = doc7.records[nom_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    sal_txt = doc7.records[sal_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    
    dx, dy = struct.unpack('<ii', doc7.records[k_rec]['payload'][:8])
    
    # check color
    nom_col = ""
    for c in range(nom_rec - 20, nom_rec):
        if doc7.records[c]['tag'] == 150:
            nom_col = doc7.records[c]['payload'].hex()
            
    col_label = "CR (Green)" if nom_col == 'd6030000' else "DB (Black)"
    
    print(f"Row {r_no:2d} | {d_txt} {t_txt:12s} | {u_txt:24s} | Nom: {nom_txt:15s} [{col_label}] | Saldo: {sal_txt:13s} (dx={dx:5d}, dy={dy:7d})")
