import sys
import os
import ctypes

is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
with open(r"C:\Users\Lenovo\xara_copilot\elevated_check.txt", "w") as f:
    f.write(f"ADMIN={is_admin}\n")
