import os
from xar_dom_engine import XarDocument

sep_xar = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Sep\0.xar"
doc = XarDocument(sep_xar)

print("=== AUDIT SUMMARY SEPTEMBER 2026 ===")
print(f"Total Records: {len(doc.records)}")

# Helper to get text and color from dict record
def get_text(r):
    data = r['payload']
    try:
        return data[4:].decode('utf-8').rstrip('\x00')
    except:
        return ""

def get_color(doc, rec_idx):
    # look back for tag 150
    for i in range(rec_idx, max(0, rec_idx-25), -1):
        if doc.records[i]['tag'] == 150:
            return doc.records[i]['payload'].hex()
    return "unknown"

# 1. Header Page 1
print("\n--- Header Page 1 ---")
print("Nama (1008):", get_text(doc.records[1008]))
print("Periode (1038, 1043):", f"'{get_text(doc.records[1038])}'", f"'{get_text(doc.records[1043])}'")
print("No Rekening (1064):", get_text(doc.records[1064]))
print("Dicetak Pada (1102):", get_text(doc.records[1102]))
print("Halaman (1124, 1242, 1263, 1268):", get_text(doc.records[1124]), get_text(doc.records[1242]), get_text(doc.records[1263]), get_text(doc.records[1268]))

# 2. Summary
print("\n--- Summary ---")
print("Saldo Awal (1147):", get_text(doc.records[1147]), "Color:", get_color(doc, 1147))
print("Dana Masuk (1157):", get_text(doc.records[1157]), "Color:", get_color(doc, 1157))
print("Dana Keluar (1170, 1171, 1176):", get_text(doc.records[1170]), f"'{get_text(doc.records[1171])}'", f"'{get_text(doc.records[1176])}'", "Color:", get_color(doc, 1170))
print("Saldo Akhir (1189):", get_text(doc.records[1189]), "Color:", get_color(doc, 1189))

# 3. Header Page 2
print("\n--- Header Page 2 ---")
print("Nama (3728):", get_text(doc.records[3728]))
print("Periode (3770, 3774, 3782):", f"'{get_text(doc.records[3770])}'", f"'{get_text(doc.records[3774])}'", f"'{get_text(doc.records[3782])}'")
print("No Rekening (3748):", get_text(doc.records[3748]))
print("Dicetak Pada (3786):", get_text(doc.records[3786]))
print("Halaman (3808, 3816, 3837, 3858, 3863):", get_text(doc.records[3808]), get_text(doc.records[3816]), get_text(doc.records[3837]), get_text(doc.records[3858]), get_text(doc.records[3863]))

# 4. Transactions (13 Rows)
saldo_records = [1543, 1685, 1839, 2001, 2175, 2332, 2469, 2611, 2758, 2928, 4104, 4258, 4405]
nominal_records = [1564, 1706, 1860, 2022, 2196, 2353, 2490, 2632, 2779, 2949, 4125, 4279, 4426]
date_records = [1614, 1751, 1910, 2062, 2236, 2403, 2545, 2687, 2829, 2999, 4170, 4329, 4471]

print("\n--- Transactions (13 Rows) ---")
for i, (s_idx, n_idx, d_idx) in enumerate(zip(saldo_records, nominal_records, date_records), 1):
    s_text = get_text(doc.records[s_idx])
    s_col = get_color(doc, s_idx)
    n_text = get_text(doc.records[n_idx])
    n_col = get_color(doc, n_idx)
    d_text = get_text(doc.records[d_idx])
    print(f"Row {i:2d} | Tgl: {d_text:<12} | Nom: {n_text:<16} (Col: {n_col}) | Saldo: {s_text:<16} (Col: {s_col})")

print("\nAudit check completed.")
