import os
import shutil
from xar_dom_engine import XarDocument

file_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"

doc = XarDocument(file_path)

trans1_before = next(t for t in doc.get_transactions() if t["row"] == 1)
print("=== SEBELUM UPDATE TRANSAKSI 1 ===")
print(f"  Nominal: {trans1_before['nominal']}")
print(f"  Saldo  : {trans1_before['balance']}")

# Targets from user
new_nom = "-1.000.000,00"
new_bal = "15.927.222,00"

print(f"\n[*] Mengubah Nominal menjadi '{new_nom}' dan Saldo menjadi '{new_bal}'...")
doc.update_nominal(1, new_nom)
doc.update_balance(1, new_bal)

# Save
doc.save(file_path)

# Verify reloaded
doc_verify = XarDocument(file_path)
trans1_after = next(t for t in doc_verify.get_transactions() if t["row"] == 1)
print("\n=== SESUDAH UPDATE TRANSAKSI 1 (VERIFIKASI RELOAD DARI DISK) ===")
print(f"  Nominal: {trans1_after['nominal']}")
print(f"  Saldo  : {trans1_after['balance']}")

# Check right edge alignment with Row 2, 3, etc.
print("\n=== PEMERIKSAAN KESELARASAN SISI KANAN (RIGHT-ALIGNMENT) ===")
print(f"{'Row':4s} | {'Nominal':16s} | {'Nom Right':10s} | {'Balance':16s} | {'Bal Right':10s}")
print("-" * 65)
for t in doc_verify.get_transactions()[:5]: # Show first 5 rows
    ns = t["nom_story"]
    bs = t["bal_story"]
    nom_r = ns["x"] + doc_verify.records[ns["line_indices"][0]]["size"] # approx or from ints
    import struct
    lrec_n = doc_verify.records[ns["line_indices"][0]]
    w_n = struct.unpack("<i", lrec_n["payload"][:4])[0]
    lrec_b = doc_verify.records[bs["line_indices"][0]]
    w_b = struct.unpack("<i", lrec_b["payload"][:4])[0]
    print(f"{t['row']:4d} | {t['nominal']:16s} | {ns['x'] + w_n:10d} | {t['balance']:16s} | {bs['x'] + w_b:10d}")
