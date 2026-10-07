"""
Xara Co-Pilot: Eksekutor Bedah Transaksi 10 (Koordinat Visual Terverifikasi)
==========================================================================
Target: Transaksi nomor 10.
Posisi Live Terverifikasi:
  - Pecahan 1 ('21'): (X=142, Y=640)
  - Pecahan 2 (':55:12 WIB'): (X=175, Y=640)
  - Garis Patokan Kiri: X=138 (sama persis dengan Row 9 di atasnya)

Langkah:
  1. Hapus '21' pada (142, 640).
  2. Buka ':55:12 WIB' pada (175, 640), ganti dengan '23:05:11 WIB'.
  3. Nudge ke kiri 12x agar tepi kiri '23' sejajar di X=138 dengan Row 9.
"""

import os
import sys
import time
import ctypes

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from xara_bridge_service import XaraBridge, user32, VK_CONTROL, VK_SHIFT, VK_ESCAPE

VK_DELETE = 0x2E
VK_LEFT = 0x25

class DualLogger:
    def __init__(self, filepath):
        self.terminal = sys.stdout
        self.logfile = open(filepath, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.logfile.write(message)
        self.logfile.flush()

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()

log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "admin_test_log.txt")
sys.stdout = DualLogger(log_path)
sys.stderr = sys.stdout

def run_trans10_bedah():
    print("=================================================================")
    print("   XARA SURGICAL CO-PILOT: PERBAIKAN TRANSAKSI 10 (LIVE)")
    print("=================================================================\n")

    is_admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
    print(f"[*] Hak Akses Python: {'ADMINISTRATOR (Elevated)' if is_admin else 'USER BIASA (Non-Elevated)'}")
    if not is_admin:
        print("[!] PERINGATAN: Jalankan melalui 'run_copilot_admin.bat' agar event mouse/keyboard diterima Xara.\n")

    bridge = XaraBridge()
    user32.SwitchToThisWindow(bridge.hwnd, True)
    time.sleep(0.5)

    print("=== 1. STATUS XARA ===")
    st = bridge.get_status()
    for k, v in st.items():
        print(f"  {k}: {v}")

    # Koordinat fisik live terverifikasi:
    x_part1, y_part1 = 142, 640
    x_part2, y_part2 = 175, 640

    print("\n=== 2. MEMFOKUSKAN XARA & CAPTURE AWAL ===")
    bridge.focus()
    time.sleep(0.3)
    pre_cap = r"C:\Users\Lenovo\xara_copilot\pre_trans10_live.png"
    bridge.capture_screenshot(pre_cap)
    print(f"Screenshot awal: {pre_cap}")

    print("\n=== 3. EKSEKUSI BEDAH KANIBALISASI & REPOSISI ===")
    print("[1] Menetralkan kanvas...")
    bridge.exit_text_editing()
    time.sleep(0.2)

    print(f"[2] Memilih pecahan '21' pada ({x_part1}, {y_part1}) dan menghapusnya...")
    bridge.click_at(x_part1, y_part1)
    time.sleep(0.25)
    bridge.send_shortcut([], VK_DELETE)
    time.sleep(0.3)

    print(f"[3] Memilih pecahan kedua pada ({x_part2}, {y_part2}) dan mengedit teks...")
    bridge.double_click_at(x_part2, y_part2)
    time.sleep(0.3)
    bridge.send_shortcut([VK_CONTROL], 0x41) # Ctrl+A
    time.sleep(0.15)
    bridge._paste_text("23:05:11 WIB")
    time.sleep(0.3)

    print("[4] Menyelesaikan mode edit teks (Escape)...")
    bridge.exit_text_editing()
    time.sleep(0.3)

    print("[5] Melakukan reposisi ke kiri (12x Nudge) agar lurus dengan Row 9...")
    bridge.click_at(x_part2, y_part2)
    time.sleep(0.2)
    for _ in range(12):
        bridge.send_shortcut([], VK_LEFT)
        time.sleep(0.03)

    bridge.exit_text_editing()
    print("[6] Selesai! Objek diselaraskan.")

    print("\n=== 4. CAPTURE HASIL AKHIR ===")
    time.sleep(0.5)
    post_cap = r"C:\Users\Lenovo\xara_copilot\post_trans10_live.png"
    bridge.capture_screenshot(post_cap)
    print(f"Screenshot akhir tersimpan: {post_cap}")

    print("\n=================================================================")
    print("                     OPERASI SELESAI")
    print("=================================================================")
    return True

if __name__ == "__main__":
    run_trans10_bedah()
