import os
import json
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
doc = XarDocument(xar_path)

with open("perfect_34_rows_map.json", "r", encoding="utf-8") as f:
    rows = json.load(f)

GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

print("=== NATIVE TAG 150 COLORS ===")
colors_found = {}
for r in rows:
    # Nom color
    nom_c_idx = r['nom_tag150']
    if nom_c_idx:
        c_hex = doc.records[nom_c_idx]['payload'].hex()
        is_cr = r['orig_nom'].startswith('+')
        k = 'Kredit (+)' if is_cr else 'Debit (-)'
        colors_found[k] = (nom_c_idx, c_hex)
    
    # Saldo color
    saldo_c_idx = r['saldo_tag150']
    if saldo_c_idx:
        c_hex = doc.records[saldo_c_idx]['payload'].hex()
        colors_found['Saldo Berjalan'] = (saldo_c_idx, c_hex)

for k, v in colors_found.items():
    print(f"  {k:20s}: Rec {v[0]:05d} -> bytearray.fromhex('{v[1]}')")

print("\n=== NATIVE RULER TARGETS ===")
nom_x_rights = []
saldo_x_rights = []

for r in rows:
    # Nom matrix
    m_idx = r['nom_tag2100']
    if m_idx:
        x, y, f = struct.unpack('<iii', doc.records[m_idx]['payload'][:12])
        w = calc_text_width(r['orig_nom'])
        xr = x + w
        nom_x_rights.append(xr)
    
    # Saldo matrix
    m_idx = r['saldo_tag2100']
    if m_idx:
        x, y, f = struct.unpack('<iii', doc.records[m_idx]['payload'][:12])
        w = calc_text_width(r['orig_saldo'])
        xr = x + w
        saldo_x_rights.append(xr)

avg_nom_xr = sum(nom_x_rights) / len(nom_x_rights)
avg_saldo_xr = sum(saldo_x_rights) / len(saldo_x_rights)

print(f"Nominal X-Right values: min={min(nom_x_rights)}, max={max(nom_x_rights)}, avg={avg_nom_xr:.0f} mp ({avg_nom_xr/28346.4567:.3f} cm)")
print(f"Saldo X-Right values  : min={min(saldo_x_rights)}, max={max(saldo_x_rights)}, avg={avg_saldo_xr:.0f} mp ({avg_saldo_xr/28346.4567:.3f} cm)")
