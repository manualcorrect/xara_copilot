from verify_exact_widths import glyph_map

def get_text_width(txt):
    return sum(glyph_map.get(c, 4800) for c in txt)

nom1 = "-100.000,00"
sal1 = "554.955,00"

w_nom1 = get_text_width(nom1)
w_sal1 = get_text_width(sal1)

print(f"Row 1 Nominal '{nom1}': width = {w_nom1} mp ({w_nom1/28346.4567:.3f} cm)")
print(f"Row 1 Saldo   '{sal1}': width = {w_sal1} mp ({w_sal1/28346.4567:.3f} cm)")

# Let's check Row 1 in test_v2.1_tahap7.xar
from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

mx_nom1 = struct.unpack('<i', doc.records[1548]['payload'][:4])[0]
kx_nom1 = struct.unpack('<i', doc.records[1564]['payload'][:4])[0]

mx_sal1 = struct.unpack('<i', doc.records[1527]['payload'][:4])[0]
kx_sal1 = struct.unpack('<i', doc.records[1543]['payload'][:4])[0]

print(f"\nDocument Tahap 7 Row 1 Values:")
print(f"  Nominal: MX = {mx_nom1} ({mx_nom1/28346.4567:.3f} cm), Tag 2206 W = {kx_nom1} ({kx_nom1/28346.4567:.3f} cm)")
print(f"           MX + Tag2206 = {mx_nom1 + kx_nom1} ({ (mx_nom1 + kx_nom1)/28346.4567:.3f} cm)")
print(f"           MX + CalcWidth = {mx_nom1 + w_nom1} ({ (mx_nom1 + w_nom1)/28346.4567:.3f} cm)")

print(f"  Saldo  : MX = {mx_sal1} ({mx_sal1/28346.4567:.3f} cm), Tag 2206 W = {kx_sal1} ({kx_sal1/28346.4567:.3f} cm)")
print(f"           MX + Tag2206 = {mx_sal1 + kx_sal1} ({ (mx_sal1 + kx_sal1)/28346.4567:.3f} cm)")
print(f"           MX + CalcWidth = {mx_sal1 + w_sal1} ({ (mx_sal1 + w_sal1)/28346.4567:.3f} cm)")
