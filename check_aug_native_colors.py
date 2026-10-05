import sys
from xar_dom_engine import XarDocument

sys.stdout.reconfigure(encoding='utf-8')

aug_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Aug"
xar_path = f"{aug_dir}\\0.xar"
doc = XarDocument(xar_path)

print("Summary Colors:")
print("Saldo Awal (rec 1218):", doc.records[1218]['payload'].hex())
print("Dana Masuk (rec 1228):", doc.records[1228]['payload'].hex())
print("Dana Keluar (rec 1239):", doc.records[1239]['payload'].hex())
print("Saldo Akhir (rec 1252):", doc.records[1252]['payload'].hex())

print("\nTable Saldo & Nominal Colors (Rows 1..5):")
for r_num, s_col, n_col in [(1, 1616, 1637), (2, 1758, 1779), (3, 1920, 1941), (4, 2082, 2103), (5, 2234, 2255)]:
    print(f"Row {r_num}: Saldo Col ({s_col}) = {doc.records[s_col]['payload'].hex()}, Nominal Col ({n_col}) = {doc.records[n_col]['payload'].hex()}")

