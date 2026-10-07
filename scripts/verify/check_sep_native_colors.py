import sys
from xar_dom_engine import XarDocument

sys.stdout.reconfigure(encoding='utf-8')

sep_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Sep"
xar_path = f"{sep_dir}\\0.xar"
doc = XarDocument(xar_path)

print("Summary Colors:")
print("Saldo Awal (rec 1142):", doc.records[1142]['payload'].hex())
print("Dana Masuk (rec 1152):", doc.records[1152]['payload'].hex())
print("Dana Keluar (rec 1163):", doc.records[1163]['payload'].hex())
print("Saldo Akhir (rec 1182):", doc.records[1182]['payload'].hex())

print("\nTable Saldo & Nominal Colors (Rows 1..5):")
for r_num, s_col, n_col in [(1, 1531, 1552), (2, 1673, 1694), (3, 1827, 1848), (4, 1989, 2010), (5, 2163, 2184)]:
    print(f"Row {r_num}: Saldo Col ({s_col}) = {doc.records[s_col]['payload'].hex()}, Nominal Col ({n_col}) = {doc.records[n_col]['payload'].hex()}")

