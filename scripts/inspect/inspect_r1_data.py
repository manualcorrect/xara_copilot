from xar_dom_engine import XarDocument
from verify_exact_widths import glyph_map

MP_PER_CM = 72000 / 2.54

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

# Let's inspect Row 1:
# Nominal: Rec 1548 (Tag 2100), Rec 1564 (Tag 2206), Rec 1565 (Tag 2201)
# Saldo  : Rec 1527 (Tag 2100), Rec 1543 (Tag 2206), Rec 1544 (Tag 2201)

import struct
mx_nom = struct.unpack('<i', doc.records[1548]['payload'][:4])[0]
w_nom_tag = struct.unpack('<i', doc.records[1564]['payload'][:4])[0]
txt_nom = doc.records[1565]['payload'].decode('utf-16le').strip('\x00')
w_nom_calc = sum(glyph_map[c] for c in txt_nom)

mx_sal = struct.unpack('<i', doc.records[1527]['payload'][:4])[0]
w_sal_tag = struct.unpack('<i', doc.records[1543]['payload'][:4])[0]
txt_sal = doc.records[1544]['payload'].decode('utf-16le').strip('\x00')
w_sal_calc = sum(glyph_map[c] for c in txt_sal)

print("ROW 1 POSITION DATA:")
print(f"Nominal: '{txt_nom}'")
print(f"  Matrix X (Left)          : {mx_nom:6d} mp ({mx_nom/MP_PER_CM:.3f} cm)")
print(f"  Tag 2206 Width           : {w_nom_tag:6d} mp ({w_nom_tag/MP_PER_CM:.3f} cm)")
print(f"  Calculated Glyph Width   : {w_nom_calc:6d} mp ({w_nom_calc/MP_PER_CM:.3f} cm)")
print(f"  Right Edge (MX + Tag2206): {mx_nom + w_nom_tag:6d} mp ({ (mx_nom + w_nom_tag)/MP_PER_CM:.3f} cm)")
print(f"  Right Edge (MX + CalcW)  : {mx_nom + w_nom_calc:6d} mp ({ (mx_nom + w_nom_calc)/MP_PER_CM:.3f} cm)")

print(f"\nSaldo: '{txt_sal}'")
print(f"  Matrix X (Left)          : {mx_sal:6d} mp ({mx_sal/MP_PER_CM:.3f} cm)")
print(f"  Tag 2206 Width           : {w_sal_tag:6d} mp ({w_sal_tag/MP_PER_CM:.3f} cm)")
print(f"  Calculated Glyph Width   : {w_sal_calc:6d} mp ({w_sal_calc/MP_PER_CM:.3f} cm)")
print(f"  Right Edge (MX + Tag2206): {mx_sal + w_sal_tag:6d} mp ({ (mx_sal + w_sal_tag)/MP_PER_CM:.3f} cm)")
print(f"  Right Edge (MX + CalcW)  : {mx_sal + w_sal_calc:6d} mp ({ (mx_sal + w_sal_calc)/MP_PER_CM:.3f} cm)")
