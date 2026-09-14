from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

print("=" * 80)
print("INSPECTING EXACT NATIVE COLORS FOR HEADERS & TABLE")
print("=" * 80)

def find_color_before(rec_idx):
    for k in range(rec_idx - 15, rec_idx):
        if doc.records[k]['tag'] == 150:
            return doc.records[k]['payload'].hex()
    return None

# Financial Summary Header nodes
print("Header Saldo Awal  (Rec 1175):", find_color_before(1175))
print("Header Dana Masuk   (Rec 1184):", find_color_before(1184))
print("Header Dana Keluar  (Rec 1202):", find_color_before(1202))
print("Header Saldo Akhir  (Rec 1215):", find_color_before(1215))

# Table samples
print("Table Saldo Row 1   (Rec 1596):", find_color_before(1596))
print("Table Nominal Row 1 (Rec 1629):", find_color_before(1629))
print("Table Saldo Row 2   (Rec 1759):", find_color_before(1759))
print("Table Nominal Row 2 (Rec 1792):", find_color_before(1792))
