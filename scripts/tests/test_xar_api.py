import shutil
from xar_dom_engine import XarDocument

src = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
dst = r"C:\Users\Lenovo\Downloads\TEST_REK_DEMO.xar"

shutil.copy(src, dst)

doc = XarDocument(dst)
print("--- Before Update ---")
for t in doc.get_transactions():
    print(f"Row {t['row']:2d}: Time={t['time']:16s} | Nom={t['nominal']:11s} | Bal={t['balance']:12s}")

print("\n--- Applying Programmatic Updates ---")
# 1. Update Row 8 (originally split '09' and ':52:22 WIB') -> unified '11:22:33 WIB'
doc.update_time(8, "11:22:33 WIB")

# 2. Update Row 1 -> unified '08:15:00 WIB'
doc.update_time(1, "08:15:00 WIB")

# 3. Update Row 10 -> '23:05:11 WIB'
doc.update_time(10, "23:05:11 WIB")

# Save document
doc.save()

# Verify reloaded
doc2 = XarDocument(dst)
print("\n--- After Update (Reloaded From Disk) ---")
for t in doc2.get_transactions():
    print(f"Row {t['row']:2d}: Time={t['time']:16s} | Nom={t['nominal']:11s} | Bal={t['balance']:12s}")
