from xar_dom_engine import XarDocument
import struct

doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar')

print("=" * 80)
print("COORDINATES AND ALIGNMENT AUDIT (PAGE 5)")
print("=" * 80)

# Map row numbers to records on page 5
# Let's search all Tag 2100 around nominal and saldo
rows = [
    (50, 12689, 12722),
    (51, 12844, 12877),
    (52, 12994, 13027),
    (53, 13134, 13167),
    (54, 13287, 13320),
    (55, 13437, 13470),
    (56, 13587, 13620),
    (57, 13739, 13772),
    (58, 13889, 13922),
]

for r_num, sal_rec, nom_rec in rows:
    sal_text = doc7.records[sal_rec]['payload'].decode('utf-16le', errors='ignore')
    nom_text = doc7.records[nom_rec]['payload'].decode('utf-16le', errors='ignore')
    
    # find parent tag 2100 before saldo
    # usually tag 2100 is around sal_rec - 6 to sal_rec + 15
    sal_mat = None
    for k in range(sal_rec - 20, sal_rec + 20):
        if doc7.records[k]['tag'] == 2100:
            sal_mat = struct.unpack('<iii', doc7.records[k]['payload'][:12])
            break
            
    nom_mat = None
    for k in range(nom_rec - 20, nom_rec + 20):
        if doc7.records[k]['tag'] == 2100:
            nom_mat = struct.unpack('<iii', doc7.records[k]['payload'][:12])
            break
            
    # Also find tag 2206 if any
    nom_adv = None
    for k in range(nom_rec - 5, nom_rec + 5):
        if doc7.records[k]['tag'] == 2206:
            nom_adv = struct.unpack('<iii', doc7.records[k]['payload'][:12])[0]
            break
            
    sal_x_cm = sal_mat[0] * 2.54 / 72000 if sal_mat else 0
    nom_x_cm = nom_mat[0] * 2.54 / 72000 if nom_mat else 0
    
    print(f"Row {r_num:2d} | Saldo: '{sal_text:13s}' (X={sal_x_cm:.3f}cm, mat={sal_mat}) | Nominal: '{nom_text:17s}' (X={nom_x_cm:.3f}cm, mat={nom_mat}, adv={nom_adv})")
