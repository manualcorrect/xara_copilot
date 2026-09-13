import os
import shutil
from xar_dom_engine import XarDocument

file_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
backup_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY_backup.xar"

# 1. Create safety backup
shutil.copy(file_path, backup_path)
print(f"[*] Backup created: {backup_path}")

# 2. Load document
doc = XarDocument(file_path)
trans1_before = next(t for t in doc.get_transactions() if t["row"] == 1)
print(f"\n[SEBELUM] Transaksi 1:")
print(f"  Tanggal : {trans1_before['date']}")
print(f"  Jam     : {trans1_before['time']} (Status: {'Pecah 2 Objek' if len(trans1_before['time_stories']) > 1 else '1 Objek'})")
print(f"  Nominal : {trans1_before['nominal']}")
print(f"  Saldo   : {trans1_before['balance']}")

# 3. Update time to 07:15:20 WIB
NEW_TIME = "07:15:20 WIB"
print(f"\n[*] Mengubah jam Transaksi 1 menjadi '{NEW_TIME}'...")
doc.update_time(1, NEW_TIME)

# 4. Save directly
doc.save(file_path)

# 5. Reload and verify from disk
doc_verify = XarDocument(file_path)
trans1_after = next(t for t in doc_verify.get_transactions() if t["row"] == 1)
print(f"\n[SESUDAH] Transaksi 1 (Verifikasi reload dari disk):")
print(f"  Tanggal : {trans1_after['date']}")
print(f"  Jam     : {trans1_after['time']} (Status: {'Pecah 2 Objek' if len(trans1_after['time_stories']) > 1 else '1 Objek Utuh'})")
print(f"  Nominal : {trans1_after['nominal']}")
print(f"  Saldo   : {trans1_after['balance']}")

time_story = trans1_after["time_stories"][0]
print(f"\n[VERIFIKASI KOORDINAT XARA]:")
print(f"  Posisi X : {time_story['x']} millipoints (Standar kolom: 51941) -> {'MATCH 100%' if time_story['x'] == 51941 else 'MISMATCH'}")
print(f"  Posisi Y : {time_story['y']} millipoints")
print(f"  Isi Teks : {time_story['full_text']}")

print("\n--- STATUS 10 TRANSAKSI SETELAH UPDATE ---")
for t in doc_verify.get_transactions():
    print(f"Row {t['row']:2d} | Date: {t['date']:11s} | Time: {t['time']:16s} | Nom: {t['nominal']:11s} | Bal: {t['balance']:12s}")
