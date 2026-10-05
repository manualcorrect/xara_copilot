from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0_backup_original.xar"
doc = XarDocument(path)

# Let's inspect saldo color nodes in the original 0.xar
saldo_color_nodes = [1576, 1733, 1900, 2072, 2249, 2391, 2548, 2720, 2901, 3038, 4147, 4291, 4433, 4575, 4722, 4894, 5041, 5209, 5341]
for i, rec_idx in enumerate(saldo_color_nodes, 1):
    col = doc.records[rec_idx]['payload'].hex()
    print(f"Row {i:2d} Saldo Color (Rec {rec_idx}): {col}")

# Also check summary saldo akhir
print("Summary Saldo Akhir (Rec 1220):", doc.records[1220]['payload'].hex())
