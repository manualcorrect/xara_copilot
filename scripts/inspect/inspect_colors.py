from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

# Tag 150 colors in summary & table
print("Summary colors:")
print("Saldo Awal (rec 1189):", doc.records[1189]['payload'].hex())
print("Dana Masuk (rec 1198):", doc.records[1198]['payload'].hex())
print("Dana Keluar (rec 1208):", doc.records[1208]['payload'].hex())
print("Saldo Akhir (rec 1220):", doc.records[1220]['payload'].hex())

# Check table nominal colors:
print("\nTable nominal colors:")
for i in [1604, 1754, 1921, 2093, 2270, 2412, 2569, 2741, 2922, 3059, 4168, 4312, 4454, 4596, 4743, 4915, 5062, 5230, 5362]:
    print(f"Rec {i}: {doc.records[i]['payload'].hex()}")

