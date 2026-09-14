from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

dicetak_recs = [1057, 3702, 6486, 9210, 11930, 14706, 17449, 20249]

print("=" * 80)
print("VERIFYING DICETAK PADA DAY NODES ACROSS ALL 8 PAGES")
print("=" * 80)

for p_idx, r_idx in enumerate(dicetak_recs, 1):
    # find tens (r_idx - 12) and units (r_idx - 8)
    tens_rec = r_idx - 12
    units_rec = r_idx - 8
    t_val = doc.records[tens_rec]['payload'].decode('utf-16le', errors='ignore')
    u_val = doc.records[units_rec]['payload'].decode('utf-16le', errors='ignore')
    m_val = doc.records[r_idx]['payload'].decode('utf-16le', errors='ignore')
    print(f"Page {p_idx} | Rec {tens_rec}='{t_val}' + Rec {units_rec}='{u_val}' + Rec {r_idx}='{m_val}' -> Full: '{t_val}{u_val} {m_val}'")
