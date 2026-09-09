"""
Xara Antigravity Co-Pilot Engine (xara_bridge_service.py)
=========================================================
Modul jembatan (bridge) deterministik antara Google Antigravity dan Xara Designer Pro+.
Menyediakan antarmuka otomasi dokumen, penggantian teks berbasis SearchDlg, ekspor PDF,
serta zero-token real-time state observer.
"""

import ctypes
from ctypes import wintypes
import time
import os
import sys
import threading
import argparse

# Win32 APIs
user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32
gdi32 = ctypes.windll.gdi32
advapi32 = ctypes.windll.advapi32

# 64-bit safe Win32 API prototypes
kernel32.GlobalAlloc.restype = ctypes.c_void_p
kernel32.GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
kernel32.GlobalLock.restype = ctypes.c_void_p
kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
user32.GetClipboardData.restype = ctypes.c_void_p
user32.GetClipboardData.argtypes = [wintypes.UINT]
user32.SetClipboardData.restype = ctypes.c_void_p
user32.SetClipboardData.argtypes = [wintypes.UINT, ctypes.c_void_p]

# Constants
ACCESS_ALL = 0x1FF
SW_RESTORE = 9
SW_SHOWMAXIMIZED = 3
SRCCOPY = 0x00CC0020
SM_CXSCREEN = 0
SM_CYSCREEN = 1

# Input Constants
INPUT_MOUSE = 0
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_SCANCODE = 0x0008

VK_MENU = 0x12       # Alt
VK_CONTROL = 0x11    # Ctrl
VK_SHIFT = 0x10      # Shift
VK_RETURN = 0x0D     # Enter
VK_ESCAPE = 0x1B     # Esc
VK_TAB = 0x09        # Tab
VK_BACK = 0x08       # Backspace

WM_SETTEXT = 0x000C
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E
WM_COMMAND = 0x0111
BM_CLICK = 0x00F5
WM_CLOSE = 0x0010

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ('dx', wintypes.LONG),
        ('dy', wintypes.LONG),
        ('mouseData', wintypes.DWORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG))
    ]

class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ('wVk', wintypes.WORD),
        ('wScan', wintypes.WORD),
        ('dwFlags', wintypes.DWORD),
        ('time', wintypes.DWORD),
        ('dwExtraInfo', ctypes.POINTER(wintypes.ULONG))
    ]

class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ('uMsg', wintypes.DWORD),
        ('wParamL', wintypes.WORD),
        ('wParamH', wintypes.WORD)
    ]

class INPUT(ctypes.Structure):
    class _U(ctypes.Union):
        _fields_ = [('mi', MOUSEINPUT), ('ki', KEYBDINPUT), ('hi', HARDWAREINPUT)]
    _anonymous_ = ('_u',)
    _fields_ = [
        ('type', wintypes.DWORD),
        ('_u', _U)
    ]

class XaraBridge:
    """Kontroler Eksekusi Deterministik untuk Xara Designer Pro+"""

    def __init__(self, target_title_substr="Xara"):
        self.target_title_substr = target_title_substr
        self.hwnd = None
        self.pid = None
        self.is_elevated = False
        self.hdesk = None
        self._attach_desktop()
        self.connect()

    def _attach_desktop(self):
        """Menghubungkan thread saat ini ke desktop interaktif default."""
        try:
            self.hdesk = user32.OpenDesktopW("default", 0, False, ACCESS_ALL)
            if self.hdesk:
                user32.SetThreadDesktop(self.hdesk)
        except Exception as e:
            print(f"[XaraBridge] Warning: gagal switch desktop: {e}")

    def connect(self):
        """Mencari dan memverifikasi jendela Xara Designer Pro+."""
        self._attach_desktop()
        found_hwnd = None
        found_pid = None

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def enum_cb(hwnd, lparam):
            nonlocal found_hwnd, found_pid
            if user32.IsWindowVisible(hwnd):
                cls = ctypes.create_unicode_buffer(256)
                user32.GetClassNameW(hwnd, cls, 256)
                if "XTPMainFrame" in cls.value:
                    title = ctypes.create_unicode_buffer(512)
                    user32.GetWindowTextW(hwnd, title, 512)
                    if self.target_title_substr.lower() in title.value.lower() or "designer" in title.value.lower():
                        found_hwnd = hwnd
                        pid = wintypes.DWORD()
                        user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                        found_pid = pid.value
                        return False
            return True

        if self.hdesk:
            user32.EnumDesktopWindows(self.hdesk, WNDENUMPROC(enum_cb), 0)

        self.hwnd = found_hwnd
        self.pid = found_pid

        if self.hwnd and self.pid:
            self._check_elevation()
            return True
        return False

    def _check_elevation(self):
        """Memeriksa apakah proses Xara berjalan elevated (Administrator)."""
        try:
            hProc = kernel32.OpenProcess(0x1000, False, self.pid)
            if hProc:
                hToken = wintypes.HANDLE()
                if advapi32.OpenProcessToken(hProc, 0x0008, ctypes.byref(hToken)):
                    elev = wintypes.DWORD()
                    retLen = wintypes.DWORD()
                    if advapi32.GetTokenInformation(hToken, 20, ctypes.byref(elev), 4, ctypes.byref(retLen)):
                        self.is_elevated = bool(elev.value)
                    kernel32.CloseHandle(hToken)
                kernel32.CloseHandle(hProc)
        except Exception:
            self.is_elevated = False

    def get_status(self):
        """Mengembalikan status detail instans Xara."""
        if not self.hwnd:
            self.connect()

        if not self.hwnd:
            return {"connected": False, "message": "Jendela Xara Designer Pro+ tidak ditemukan."}

        title_buf = ctypes.create_unicode_buffer(512)
        user32.GetWindowTextW(self.hwnd, title_buf, 512)
        title = title_buf.value

        rect = wintypes.RECT()
        user32.GetWindowRect(self.hwnd, ctypes.byref(rect))

        is_dirty = "*" in title

        return {
            "connected": True,
            "hwnd": f"0x{self.hwnd:X}",
            "pid": self.pid,
            "title": title,
            "is_dirty": is_dirty,
            "is_elevated": self.is_elevated,
            "rect": [rect.left, rect.top, rect.right - rect.left, rect.bottom - rect.top]
        }

    def focus(self):
        """Membawa jendela Xara ke latar depan secara deterministik."""
        if not self.hwnd:
            if not self.connect():
                return False

        self._attach_desktop()

        # 1. Unlock foreground lock via Alt tap & LockSetForegroundWindow
        user32.LockSetForegroundWindow(1) # LSFW_UNLOCK = 1
        user32.keybd_event(VK_MENU, 0, 0, 0)
        user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)

        fore_hwnd = user32.GetForegroundWindow()
        fore_pid = wintypes.DWORD()
        fore_thread = user32.GetWindowThreadProcessId(fore_hwnd, ctypes.byref(fore_pid))
        my_thread = kernel32.GetCurrentThreadId()
        target_pid = wintypes.DWORD()
        target_thread = user32.GetWindowThreadProcessId(self.hwnd, ctypes.byref(target_pid))

        if fore_thread != my_thread:
            user32.AttachThreadInput(my_thread, fore_thread, True)
        if target_thread != my_thread:
            user32.AttachThreadInput(my_thread, target_thread, True)

        user32.ShowWindow(self.hwnd, SW_RESTORE)
        user32.ShowWindow(self.hwnd, SW_SHOWMAXIMIZED)
        user32.BringWindowToTop(self.hwnd)
        ret = user32.SetForegroundWindow(self.hwnd)
        user32.SetFocus(self.hwnd)

        if fore_thread != my_thread:
            user32.AttachThreadInput(my_thread, fore_thread, False)
        if target_thread != my_thread:
            user32.AttachThreadInput(my_thread, target_thread, False)

        time.sleep(0.3)
        cur = user32.GetForegroundWindow()
        success = (cur == self.hwnd)
        print(f"[XaraBridge] focus() -> target: 0x{self.hwnd:X}, active: 0x{cur:X}, match: {success}")
        return success

    def send_shortcut(self, keys_down, key_press):
        """Mengirim kombinasi tombol secara deterministik via keybd_event."""
        for k in keys_down:
            user32.keybd_event(k, 0, 0, 0)
            time.sleep(0.02)
        user32.keybd_event(key_press, 0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(key_press, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.02)
        for k in reversed(keys_down):
            user32.keybd_event(k, 0, KEYEVENTF_KEYUP, 0)
            time.sleep(0.02)

    def send_keys_combo(self, keys_down, key_press):
        """Kompatibilitas alias untuk send_shortcut."""
        self.send_shortcut(keys_down, key_press)

    def exit_text_editing(self):
        """Memastikan Xara keluar dari mode inline text cursor menuju Selector Tool."""
        print("[XaraBridge] Menetralkan seleksi & kursor teks (Esc 2x + F2)...")
        # Esc 1
        user32.keybd_event(VK_ESCAPE, 0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.1)
        # Esc 2
        user32.keybd_event(VK_ESCAPE, 0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.15)
        # F2 (Selector Tool)
        user32.keybd_event(0x71, 0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(0x71, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.2)

    def _find_search_dialog(self):
        """Mencari dialog SearchDlg di top-level maupun child windows."""
        found = []

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def enum_win(h, lp):
            if user32.IsWindowVisible(h):
                pid = wintypes.DWORD()
                user32.GetWindowThreadProcessId(h, ctypes.byref(pid))
                if pid.value == self.pid and h != self.hwnd:
                    cls = ctypes.create_unicode_buffer(256)
                    user32.GetClassNameW(h, cls, 256)
                    title = ctypes.create_unicode_buffer(256)
                    user32.GetWindowTextW(h, title, 256)
                    t_low = title.value.lower()
                    c_low = cls.value.lower()
                    if any(w in t_low for w in ["find", "search", "replace", "cari", "ganti"]) or "#32770" in c_low:
                        found.append((h, cls.value, title.value))
            return True

        user32.EnumWindows(WNDENUMPROC(enum_win), 0)
        if self.hdesk:
            user32.EnumDesktopWindows(self.hdesk, WNDENUMPROC(enum_win), 0)
        user32.EnumChildWindows(self.hwnd, WNDENUMPROC(enum_win), 0)

        if found:
            return found[0]
        return None

    def open_search_dialog(self, timeout=4.0):
        """Membuka dialog SearchDlg dengan multi-tier fallback."""
        self.exit_text_editing()

        # Strategi 1: Ctrl + Alt + F (Shortcut standar Selector Tool)
        print("[XaraBridge] [Strategi 1] Mencoba shortcut Ctrl+Alt+F...")
        self.send_shortcut([VK_CONTROL, VK_MENU], 0x46)
        t_end = time.time() + 1.2
        while time.time() < t_end:
            dlg = self._find_search_dialog()
            if dlg:
                print(f"[XaraBridge] SearchDlg terdeteksi via Strategi 1: HWND 0x{dlg[0]:X} Class='{dlg[1]}' Title='{dlg[2]}'")
                return dlg[0]
            time.sleep(0.1)

        # Strategi 2: Ctrl + F (Shortcut saat Text Tool aktif)
        print("[XaraBridge] [Strategi 2] Mencoba shortcut Ctrl+F...")
        self.send_shortcut([VK_CONTROL], 0x46)
        t_end = time.time() + 1.2
        while time.time() < t_end:
            dlg = self._find_search_dialog()
            if dlg:
                print(f"[XaraBridge] SearchDlg terdeteksi via Strategi 2: HWND 0x{dlg[0]:X} Class='{dlg[1]}' Title='{dlg[2]}'")
                return dlg[0]
            time.sleep(0.1)

        # Strategi 3: Menu Edit -> Find (Alt + E, lalu F)
        print("[XaraBridge] [Strategi 3] Mencoba via Menu Alt+E, lalu F...")
        user32.keybd_event(VK_MENU, 0, 0, 0)
        time.sleep(0.04)
        user32.keybd_event(0x45, 0, 0, 0) # 'E'
        time.sleep(0.04)
        user32.keybd_event(0x45, 0, KEYEVENTF_KEYUP, 0)
        user32.keybd_event(VK_MENU, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.3)
        user32.keybd_event(0x46, 0, 0, 0) # 'F'
        time.sleep(0.04)
        user32.keybd_event(0x46, 0, KEYEVENTF_KEYUP, 0)

        t_end = time.time() + 1.5
        while time.time() < t_end:
            dlg = self._find_search_dialog()
            if dlg:
                print(f"[XaraBridge] SearchDlg terdeteksi via Strategi 3: HWND 0x{dlg[0]:X} Class='{dlg[1]}' Title='{dlg[2]}'")
                return dlg[0]
            time.sleep(0.1)

        return None

    def click_at(self, x, y):
        """Mengirim klik kiri pada koordinat layar (x, y)."""
        user32.SetCursorPos(x, y)
        time.sleep(0.04)
        user32.mouse_event(0x0002, 0, 0, 0, 0) # MOUSEEVENTF_LEFTDOWN
        time.sleep(0.04)
        user32.mouse_event(0x0004, 0, 0, 0, 0) # MOUSEEVENTF_LEFTUP
        time.sleep(0.04)

    def double_click_at(self, x, y):
        """Mengirim klik ganda pada koordinat layar (x, y)."""
        self.click_at(x, y)
        time.sleep(0.06)
        self.click_at(x, y)
        time.sleep(0.1)

    def set_clipboard_text(self, text):
        """Menyimpan teks ke Clipboard Win32 dengan aman (64-bit Unicode)."""
        try:
            if user32.OpenClipboard(None):
                user32.EmptyClipboard()
                size = (len(text) + 1) * 2
                hcd = kernel32.GlobalAlloc(0x0042, size) # GMEM_MOVEABLE | GMEM_ZEROINIT
                if hcd:
                    pcd = kernel32.GlobalLock(hcd)
                    ctypes.memmove(pcd, text.encode('utf-16le') + b'\x00\x00', size)
                    kernel32.GlobalUnlock(hcd)
                    user32.SetClipboardData(13, hcd) # CF_UNICODETEXT
                user32.CloseClipboard()
        except Exception as e:
            print(f"[XaraBridge] Warning set clipboard: {e}")

    def get_clipboard_text(self):
        """Membaca teks dari Clipboard Win32 (64-bit Unicode)."""
        t = ""
        try:
            if user32.OpenClipboard(None):
                h = user32.GetClipboardData(13) # CF_UNICODETEXT
                if h:
                    p = kernel32.GlobalLock(h)
                    if p:
                        t = ctypes.wstring_at(p)
                        kernel32.GlobalUnlock(h)
                user32.CloseClipboard()
        except Exception as e:
            print(f"[XaraBridge] Warning get clipboard: {e}")
        return t

    def _paste_text(self, text):
        """Memasukkan teks ke kontrol aktif via Win32 Clipboard + Ctrl+V."""
        self.set_clipboard_text(text)
        self.send_shortcut([VK_CONTROL], 0x56) # Ctrl+V
        time.sleep(0.1)

    def diagnose_text_structure(self, raw_text):
        """
        Mendiagnosis anomali penafsiran PDF pada teks terpilih:
        1. Multi-line column fusion (penyatuan baris vertikal).
        2. Missing spaces (kata melekat akibat synthetic kerning drop).
        3. Encoded / PUA glyphs (karakter acak / subset tak standar).
        """
        issues = []
        is_welded = False
        has_missing_spaces = False

        if not raw_text:
            return {"status": "EMPTY", "issues": ["Teks kosong atau tidak terseleksi."]}

        lines = [l for l in raw_text.splitlines() if l.strip()]
        if len(lines) > 1:
            is_welded = True
            issues.append(f"Multi-Line Fusion: {len(lines)} baris teks menyatu ke dalam satu objek!")

        # Deteksi kata melekat tanpa spasi (misal: 'Jumlahpenghasila', 'BiayaPiket')
        import re
        welded_words = re.findall(r'[a-z][A-Z]|[a-zA-Z]:[a-zA-Z]|[0-9][a-zA-Z]|[a-zA-Z][0-9]', raw_text)
        if welded_words:
            has_missing_spaces = True
            issues.append(f"Missing Spaces / Synthetic Kerning Drop: Terdeteksi kata melekat: {welded_words[:5]}")

        # Deteksi karakter aneh / non-ASCII di luar simbol standar
        strange_chars = [c for c in raw_text if ord(c) > 127 and c not in '’“”–—•€£¥']
        if strange_chars:
            issues.append(f"Subset / CMap Anomaly: Terdeteksi karakter di luar charset standar: {set(strange_chars)}")

        return {
            "is_welded": is_welded,
            "has_missing_spaces": has_missing_spaces,
            "line_count": len(lines),
            "lines": lines,
            "issues": issues,
            "raw_preview": repr(raw_text[:80])
        }

    def calculate_right_alignment_offset(self, old_text, new_text, font_size_pt=10.8, dpi=96):
        """
        Menghitung selisih pergeseran koordinat horizontal (sumbu X) untuk menjaga rata kanan.
        Angka tabular (0-9) biasanya memiliki lebar ~0.55 em.
        Jika digit baru lebih banyak, titik awal X harus bergeser ke kiri sebesar delta_x.
        """
        # Hitung estimasi lebar karakter tabular
        em_px = font_size_pt * (dpi / 72.0)
        digit_width_px = em_px * 0.55

        # Hitung jumlah digit & pemisah
        def get_text_width_units(s):
            digits = sum(1 for c in s if c.isdigit())
            dots = sum(1 for c in s if c in '.,')
            others = len(s) - digits - dots
            return (digits * 1.0) + (dots * 0.35) + (others * 0.5)

        w_old = get_text_width_units(old_text)
        w_new = get_text_width_units(new_text)
        delta_units = w_new - w_old
        delta_px = delta_units * digit_width_px

        return {
            "delta_px": round(delta_px, 2),
            "shift_left_px": round(max(0, delta_px), 2),
            "shift_right_px": round(max(0, -delta_px), 2),
            "recommendation": f"Geser koordinat X ke KIRI sebesar {round(delta_px, 1)} px agar tanda ',-' tetap rata kanan persis."
        }

    def inspect_element_at(self, click_x, click_y):
        """
        Memeriksa objek pada koordinat (click_x, click_y) tanpa merusak atau mengubah isinya.
        Membaca teks objek dan mengembalikan diagnosa lengkap.
        """
        if not self.focus():
            return False, "Gagal fokus ke Xara."

        print(f"[XaraBridge-Audit] Memeriksa objek pada ({click_x}, {click_y})...")
        self.exit_text_editing()
        time.sleep(0.2)

        self.double_click_at(click_x, click_y)
        time.sleep(0.3)

        # Select all teks di dalam objek
        self.send_shortcut([VK_CONTROL], 0x41) # Ctrl+A
        time.sleep(0.15)

        # Copy teks
        self.set_clipboard_text("")
        self.send_shortcut([VK_CONTROL], 0x43) # Ctrl+C
        time.sleep(0.2)
        raw_text = self.get_clipboard_text()

        # Keluar dari mode edit (Escape 2x)
        self.exit_text_editing()

        diagnosis = self.diagnose_text_structure(raw_text)
        return True, {"raw_text": raw_text, "diagnosis": diagnosis}

    def create_simple_line_text(self, click_x, click_y, text, reference_coords=None):
        """
        Membuat objek teks baru mandiri (Simple Line Text):
        1. Aktifkan Text Tool (F8).
        2. Klik 1 KALI pada canvas (bukan drag kotak, agar anti line-wrap).
        3. Ketikkan / Paste teks baru.
        4. Jika reference_coords diberikan, kloning atribut (Ctrl+Shift+A) dari elemen referensi.
        """
        if not self.focus():
            return False, "Gagal fokus ke Xara."

        print(f"[XaraBridge-Surgical] Membuat Simple Line Text pada ({click_x}, {click_y}) berisi: '{text}'...")
        self.exit_text_editing()
        time.sleep(0.2)

        # 1. Aktifkan Text Tool via shortcut F8 (VK_F8 = 0x77)
        print("[XaraBridge-Surgical] Mengaktifkan Text Tool (F8)...")
        self.send_shortcut([], 0x77) # F8
        time.sleep(0.2)

        # 2. Klik 1 KALI pada posisi target (Simple Text)
        print(f"[XaraBridge-Surgical] Klik tunggal pada ({click_x}, {click_y})...")
        self.click_at(click_x, click_y)
        time.sleep(0.3)

        # 3. Paste teks
        print(f"[XaraBridge-Surgical] Memasukkan teks via clipboard: '{text}'...")
        self._paste_text(text)
        time.sleep(0.3)

        # 4. Netralkan kursor
        self.exit_text_editing()

        # 5. Kloning atribut jika referensi tersedia
        if reference_coords:
            ref_x, ref_y = reference_coords
            print(f"[XaraBridge-Surgical] Mengkloning atribut font/style dari referensi ({ref_x}, {ref_y})...")
            # Klik referensi
            self.click_at(ref_x, ref_y)
            time.sleep(0.2)
            self.send_shortcut([VK_CONTROL], 0x43) # Ctrl+C (Copy Attributes)
            time.sleep(0.2)
            # Klik kembali objek baru
            self.click_at(click_x, click_y)
            time.sleep(0.2)
            # Paste Attributes (Ctrl+Shift+A)
            self.send_shortcut([VK_CONTROL, VK_SHIFT], 0x41)
            time.sleep(0.3)
            self.exit_text_editing()

        return True, f"Simple Line Text '{text}' berhasil dibuat pada ({click_x}, {click_y})."

    def direct_visual_replace(self, click_x=496, click_y=593, find_val="4.380.000", replace_val="24.480.000"):
        """
        Otomasi Visual Bedah (Surgical Replacement):
        Mendeteksi struktur objek terlebih dahulu.
        Jika objek terdeteksi merupakan kluster welded yang rawan rusak,
        hanya mengganti karakter yang diperlukan secara presisi.
        """
        if not self.focus():
            return False, "Gagal fokus ke Xara."

        print(f"[XaraBridge-Visual] Memulai Penggantian Bedah ({find_val} -> {replace_val}) di ({click_x}, {click_y})...")

        # 1. Pastikan canvas siap dan mode teks netral
        self.exit_text_editing()
        time.sleep(0.3)

        # 2. Klik ganda pada teks target
        print(f"[XaraBridge-Visual] Mengklik ganda pada koordinat canvas ({click_x}, {click_y})...")
        self.double_click_at(click_x, click_y)
        time.sleep(0.4)

        # 3. Select all pada blok teks yang terbuka
        print("[XaraBridge-Visual] Menyeleksi teks pada objek aktif (Ctrl+A)...")
        self.send_shortcut([VK_CONTROL], 0x41) # Ctrl+A
        time.sleep(0.2)

        # 4. Copy ke clipboard untuk membaca teks asli
        self.set_clipboard_text("")
        self.send_shortcut([VK_CONTROL], 0x43) # Ctrl+C
        time.sleep(0.2)
        selected = self.get_clipboard_text()
        print(f"[XaraBridge-Visual] Teks terdeteksi di objek:\n{repr(selected)}")

        if not selected:
            self.exit_text_editing()
            return False, "Tidak ada teks yang terdeteksi pada objek canvas."

        # Diagnosis struktur teks
        diag = self.diagnose_text_structure(selected)
        if diag["issues"]:
            print("[XaraBridge-Visual] DIAGNOSIS ANOMALI PDF:")
            for iss in diag["issues"]:
                print(f"  * {iss}")

        # 5. Penggantian Bedah (Surgical Replacement):
        if find_val in selected:
            replacement = selected.replace(find_val, replace_val)
            print(f"[XaraBridge-Visual] Mengganti persis: '{find_val}' -> '{replace_val}'")
        else:
            import re
            pat = re.escape(find_val).replace(r'\.', r'[.,\s]?')
            m = re.search(pat, selected)
            if m:
                matched = m.group(0)
                replacement = selected[:m.start()] + replace_val + selected[m.end():]
                print(f"[XaraBridge-Visual] Mengganti kecocokan regex: '{matched}' -> '{replace_val}'")
            else:
                self.exit_text_editing()
                return False, f"Nilai '{find_val}' tidak ditemukan di dalam teks objek terpilih."

        # 6. Paste kembali teks
        print("[XaraBridge-Visual] Memasukkan teks hasil penggantian bedah (Ctrl+V)...")
        self.set_clipboard_text(replacement)
        self.send_shortcut([VK_CONTROL], 0x56) # Ctrl+V
        time.sleep(0.3)

        # 7. Selesai edit teks (Escape)
        self.exit_text_editing()

        return True, f"Nilai '{find_val}' berhasil diganti menjadi '{replace_val}'."

    def replace_text(self, find_str, replace_str):
        """Menjalankan penggantian teks menggunakan dialog SearchDlg bawaan Xara."""
        if not self.focus():
            return False, "Gagal fokus ke Xara."

        print(f"[XaraBridge] Memulai proses penggantian teks: '{find_str}' -> '{replace_str}'...")

        dlg_hwnd = self.open_search_dialog()
        if not dlg_hwnd:
            return False, "Dialog SearchDlg tidak terdeteksi terbuka setelah semua strategi."

        # Bawa dialog ke latar depan
        user32.SetForegroundWindow(dlg_hwnd)
        user32.SetFocus(dlg_hwnd)
        time.sleep(0.2)

        # Enumerate controls di dialog
        child_edits = []
        child_combos = []
        child_buttons = {}

        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
        def enum_controls(chwnd, lparam):
            cls = ctypes.create_unicode_buffer(128)
            user32.GetClassNameW(chwnd, cls, 128)
            title = ctypes.create_unicode_buffer(128)
            user32.GetWindowTextW(chwnd, title, 128)
            c_name = cls.value.lower()
            t_name = title.value.strip()

            if "edit" in c_name:
                child_edits.append((chwnd, t_name))
            elif "combobox" in c_name:
                child_combos.append(chwnd)
            elif "button" in c_name:
                child_buttons[t_name.lower()] = chwnd
            return True

        user32.EnumChildWindows(dlg_hwnd, WNDENUMPROC(enum_controls), 0)

        print(f"[XaraBridge] Kontrol dialog ditemukan: {len(child_edits)} Edits, {len(child_combos)} ComboBoxes, {len(child_buttons)} Buttons ({list(child_buttons.keys())})")

        target_edits = [e[0] for e in child_edits]
        if len(target_edits) < 2 and child_combos:
            for cb in child_combos:
                def enum_cb_child(ch, lp):
                    c = ctypes.create_unicode_buffer(64)
                    user32.GetClassNameW(ch, c, 64)
                    if "edit" in c.value.lower() and ch not in target_edits:
                        target_edits.append(ch)
                    return True
                user32.EnumChildWindows(cb, WNDENUMPROC(enum_cb_child), 0)

        if len(target_edits) >= 2:
            find_ctrl = target_edits[0]
            repl_ctrl = target_edits[1]

            # 1. Set Find Text
            user32.SendMessageW(find_ctrl, WM_SETTEXT, 0, find_str)
            parent = user32.GetParent(find_ctrl)
            ctrl_id = user32.GetDlgCtrlID(find_ctrl)
            user32.SendMessageW(parent, WM_COMMAND, (0x0300 << 16) | ctrl_id, find_ctrl)

            # 2. Set Replace Text
            user32.SendMessageW(repl_ctrl, WM_SETTEXT, 0, replace_str)
            ctrl_id2 = user32.GetDlgCtrlID(repl_ctrl)
            user32.SendMessageW(parent, WM_COMMAND, (0x0300 << 16) | ctrl_id2, repl_ctrl)
            time.sleep(0.3)

            # 3. Klik Tombol Replace All atau Replace
            replace_btn = None
            for name, bhwnd in child_buttons.items():
                if "replace all" in name or "all" in name:
                    replace_btn = bhwnd
                    break
            if not replace_btn:
                for name, bhwnd in child_buttons.items():
                    if "replace" in name or "ganti" in name:
                        replace_btn = bhwnd
                        break

            if replace_btn:
                print(f"[XaraBridge] Mengklik tombol Replace (HWND 0x{replace_btn:X})...")
                user32.SendMessageW(replace_btn, BM_CLICK, 0, 0)
                time.sleep(0.5)
            else:
                print(f"[XaraBridge] Tombol Replace tidak teridentifikasi spesifik, mengirim Alt+A...")
                self.send_shortcut([VK_MENU], 0x41)
                time.sleep(0.5)
        else:
            print("[XaraBridge] Menggunakan Fallback Keyboard Injection pada SearchDlg...")
            self.send_shortcut([VK_CONTROL], 0x41) # Ctrl+A
            time.sleep(0.05)
            self._paste_text(find_str)
            time.sleep(0.1)

            user32.keybd_event(VK_TAB, 0, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(VK_TAB, 0, KEYEVENTF_KEYUP, 0)
            time.sleep(0.1)

            self.send_shortcut([VK_CONTROL], 0x41) # Ctrl+A
            time.sleep(0.05)
            self._paste_text(replace_str)
            time.sleep(0.1)

            print("[XaraBridge] Menekan Alt+A (Replace All)...")
            self.send_shortcut([VK_MENU], 0x41)
            time.sleep(0.5)

        # Tutup dialog via Esc atau WM_CLOSE
        print("[XaraBridge] Menutup SearchDlg...")
        user32.PostMessageW(dlg_hwnd, WM_CLOSE, 0, 0)
        time.sleep(0.1)
        user32.keybd_event(VK_ESCAPE, 0, 0, 0)
        time.sleep(0.05)
        user32.keybd_event(VK_ESCAPE, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.3)

        return True, f"Teks '{find_str}' berhasil diganti menjadi '{replace_str}'."

    def save(self):
        """Menyimpan dokumen via Ctrl + S dan memverifikasi dirty flag."""
        if not self.focus():
            return False
        self.exit_text_editing()
        print("[XaraBridge] Menyimpan dokumen via Ctrl+S...")
        self.send_shortcut([VK_CONTROL], 0x53)
        time.sleep(0.8)

        st = self.get_status()
        is_dirty = st.get("is_dirty", True)
        print(f"[XaraBridge] Status setelah save: is_dirty={is_dirty} (Title: '{st.get('title')}')")
        return not is_dirty

    def export_pdf(self, output_path):
        """Mengekspor dokumen ke PDF via Shift + Ctrl + E."""
        if not self.focus():
            return False, "Gagal fokus ke Xara."

        self.exit_text_editing()
        print(f"[XaraBridge] Memanggil Export untuk: '{output_path}'...")
        self.send_shortcut([VK_SHIFT, VK_CONTROL], 0x45)
        time.sleep(1.2)

        export_dlg_hwnd = None
        WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

        def enum_dlg(hwnd, lparam):
            nonlocal export_dlg_hwnd
            if user32.IsWindowVisible(hwnd):
                cls = ctypes.create_unicode_buffer(256)
                user32.GetClassNameW(hwnd, cls, 256)
                title = ctypes.create_unicode_buffer(256)
                user32.GetWindowTextW(hwnd, title, 256)
                if ("export" in title.value.lower() or "#32770" in cls.value):
                    pid = wintypes.DWORD()
                    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
                    if pid.value == self.pid and hwnd != self.hwnd:
                        export_dlg_hwnd = hwnd
                        return False
            return True

        user32.EnumWindows(WNDENUMPROC(enum_dlg), 0)
        if self.hdesk:
            user32.EnumDesktopWindows(self.hdesk, WNDENUMPROC(enum_dlg), 0)

        if not export_dlg_hwnd:
            return False, "Dialog Export tidak terdeteksi terbuka."

        print(f"[XaraBridge] Dialog Export terdeteksi: HWND 0x{export_dlg_hwnd:X}")

        child_edits = []
        def enum_controls(chwnd, lparam):
            cls = ctypes.create_unicode_buffer(128)
            user32.GetClassNameW(chwnd, cls, 128)
            if "edit" in cls.value.lower():
                child_edits.append(chwnd)
            return True

        user32.EnumChildWindows(export_dlg_hwnd, WNDENUMPROC(enum_controls), 0)

        if child_edits:
            user32.SendMessageW(child_edits[0], WM_SETTEXT, 0, output_path)
            time.sleep(0.3)
            user32.keybd_event(VK_RETURN, 0, 0, 0)
            time.sleep(0.05)
            user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
            time.sleep(2.0)

            # Jika muncul dialog opsi PDF ("PDF Export Options"), tekan Enter untuk default
            dlg_opt = self._find_search_dialog()
            if dlg_opt:
                user32.keybd_event(VK_RETURN, 0, 0, 0)
                time.sleep(0.05)
                user32.keybd_event(VK_RETURN, 0, KEYEVENTF_KEYUP, 0)
                time.sleep(1.5)

            return True, f"Ekspor PDF berhasil diarahkan ke: '{output_path}'"
        else:
            return False, "Kotak nama berkas tidak ditemukan di dialog Export."

    def capture_screenshot(self, output_path):
        """Menangkap tangkapan layar dokumen aktif ke berkas gambar PNG/BMP."""
        self._attach_desktop()
        w = user32.GetSystemMetrics(SM_CXSCREEN)
        h = user32.GetSystemMetrics(SM_CYSCREEN)

        hdc_screen = user32.GetDC(0)
        hdc_mem = gdi32.CreateCompatibleDC(hdc_screen)
        hbm = gdi32.CreateCompatibleBitmap(hdc_screen, w, h)
        hbm_old = gdi32.SelectObject(hdc_mem, hbm)

        gdi32.BitBlt(hdc_mem, 0, 0, w, h, hdc_screen, 0, 0, SRCCOPY)

        class BITMAPINFOHEADER(ctypes.Structure):
            _fields_ = [
                ('biSize', wintypes.DWORD), ('biWidth', wintypes.LONG), ('biHeight', wintypes.LONG),
                ('biPlanes', wintypes.WORD), ('biBitCount', wintypes.WORD), ('biCompression', wintypes.DWORD),
                ('biSizeImage', wintypes.DWORD), ('biXPelsPerMeter', wintypes.LONG), ('biYPelsPerMeter', wintypes.LONG),
                ('biClrUsed', wintypes.DWORD), ('biClrImportant', wintypes.DWORD)
            ]

        bih = BITMAPINFOHEADER()
        bih.biSize = ctypes.sizeof(BITMAPINFOHEADER)
        bih.biWidth = w
        bih.biHeight = h
        bih.biPlanes = 1
        bih.biBitCount = 24
        bih.biCompression = 0
        bih.biSizeImage = ((w * 24 + 31) // 32) * 4 * h

        bmp_data = ctypes.create_string_buffer(bih.biSizeImage)
        gdi32.GetDIBits(hdc_screen, hbm, 0, h, bmp_data, ctypes.byref(bih), 0)

        class BITMAPFILEHEADER(ctypes.Structure):
            _pack_ = 2
            _fields_ = [
                ('bfType', wintypes.WORD), ('bfSize', wintypes.DWORD),
                ('bfReserved1', wintypes.WORD), ('bfReserved2', wintypes.WORD),
                ('bfOffBits', wintypes.DWORD)
            ]

        bfh = BITMAPFILEHEADER()
        bfh.bfType = 0x4D42
        bfh.bfOffBits = ctypes.sizeof(BITMAPFILEHEADER) + ctypes.sizeof(BITMAPINFOHEADER)
        bfh.bfSize = bfh.bfOffBits + bih.biSizeImage

        bmp_path = output_path if output_path.endswith('.bmp') else output_path + '.bmp'
        with open(bmp_path, "wb") as f:
            f.write(bytes(bfh))
            f.write(bytes(bih))
            f.write(bytes(bmp_data))

        gdi32.SelectObject(hdc_mem, hbm_old)
        gdi32.DeleteObject(hbm)
        gdi32.DeleteDC(hdc_mem)
        user32.ReleaseDC(0, hdc_screen)

        # Convert to PNG jika diakhiri .png
        if output_path.endswith('.png'):
            try:
                import subprocess
                ps_cmd = f"Add-Type -AssemblyName System.Drawing; $img = [System.Drawing.Image]::FromFile('{bmp_path}'); $img.Save('{output_path}', [System.Drawing.Imaging.ImageFormat]::Png); $img.Dispose();"
                subprocess.run(["powershell", "-NoProfile", "-Command", ps_cmd], check=True, stdout=subprocess.DEVNULL)
                if os.path.exists(bmp_path) and bmp_path != output_path:
                    os.remove(bmp_path)
            except Exception as e:
                print(f"[XaraBridge] Warning convert PNG: {e}")

        return os.path.exists(output_path)


class XaraObserver:
    """Sensor Pemantau 0-Token untuk Mendeteksi Suntingan Manual Pengguna."""

    def __init__(self, bridge, callback=None):
        self.bridge = bridge
        self.callback = callback
        self.running = False
        self.thread = None
        self.backup_dir = r"C:\Users\Lenovo\AppData\Local\Xara\XtremeProSub\Sub\Backups"

    def start(self, duration_seconds=60):
        """Memulai pengamatan di thread latar belakang."""
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, args=(duration_seconds,), daemon=True)
        self.thread.start()
        print(f"[XaraObserver] Dimulai selama {duration_seconds} detik (0 Token).")

    def _run_loop(self, duration_seconds):
        start_time = time.time()
        last_title = ""
        st = self.bridge.get_status()
        if st.get("connected"):
            last_title = st.get("title", "")

        last_backup_mtime = 0
        if os.path.exists(self.backup_dir):
            try:
                files = [os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir)]
                if files:
                    last_backup_mtime = max(os.path.getmtime(f) for f in files)
            except Exception:
                pass

        while self.running and (time.time() - start_time < duration_seconds):
            st = self.bridge.get_status()
            if st.get("connected"):
                cur_title = st.get("title", "")
                if cur_title != last_title:
                    event_data = {
                        "type": "TITLE_CHANGE",
                        "before": last_title,
                        "after": cur_title,
                        "is_dirty": "*" in cur_title
                    }
                    print(f"\n[XaraObserver EVENT] Perubahan Dokumen: '{last_title}' -> '{cur_title}'")
                    if self.callback:
                        self.callback(event_data)
                    last_title = cur_title

            # Cek Backups
            if os.path.exists(self.backup_dir):
                try:
                    files = [os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir)]
                    if files:
                        cur_mtime = max(os.path.getmtime(f) for f in files)
                        if cur_mtime > last_backup_mtime:
                            event_data = {
                                "type": "BACKUP_UPDATED",
                                "mtime": cur_mtime
                            }
                            print(f"\n[XaraObserver EVENT] Snapshot Dokumen Diperbarui di Backups.")
                            if self.callback:
                                self.callback(event_data)
                            last_backup_mtime = cur_mtime
                except Exception:
                    pass

            time.sleep(0.5)

        self.running = False
        print("\n[XaraObserver] Selesai.")

    def stop(self):
        self.running = False


# =====================================================================
# CLI INTERFACE
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="Xara Antigravity Co-Pilot Engine")
    subparsers = parser.add_subparsers(dest="command")

    # status
    subparsers.add_parser("status", help="Periksa koneksi dan status jendela Xara")

    # focus
    subparsers.add_parser("focus", help="Fokuskan jendela Xara ke latar depan")

    # replace
    rep_parser = subparsers.add_parser("replace", help="Ganti teks dalam dokumen Xara")
    rep_parser.add_argument("--find", required=True, help="Teks target yang dicari")
    rep_parser.add_argument("--replace", required=True, help="Teks pengganti")

    # save
    subparsers.add_parser("save", help="Simpan dokumen kerja Xara")

    # export
    exp_parser = subparsers.add_parser("export", help="Ekspor dokumen ke format PDF")
    exp_parser.add_argument("--output", required=True, help="Path lengkap berkas PDF keluaran")

    # capture
    cap_parser = subparsers.add_parser("capture", help="Ambil screenshot canvas Xara")
    cap_parser.add_argument("--output", default="xara_screenshot.png", help="Path berkas gambar")

    # watch
    watch_parser = subparsers.add_parser("watch", help="Amati perubahan dokumen manual pengguna")
    watch_parser.add_argument("--duration", type=int, default=60, help="Durasi pengamatan (detik)")

    args = parser.parse_args()

    bridge = XaraBridge()

    if args.command == "status" or not args.command:
        st = bridge.get_status()
        print("=== STATUS XARA DESIGNER PRO+ ===")
        for k, v in st.items():
            print(f"  {k}: {v}")

    elif args.command == "focus":
        res = bridge.focus()
        print(f"Focus result: {res}")

    elif args.command == "replace":
        success, msg = bridge.replace_text(args.find, args.replace)
        print(f"Replace Result: {'BERHASIL' if success else 'GAGAL'} - {msg}")

    elif args.command == "save":
        res = bridge.save()
        print(f"Save Result: {res}")

    elif args.command == "export":
        success, msg = bridge.export_pdf(args.output)
        print(f"Export Result: {'BERHASIL' if success else 'GAGAL'} - {msg}")

    elif args.command == "capture":
        res = bridge.capture_screenshot(args.output)
        print(f"Capture Result: {'BERHASIL' if res else 'GAGAL'} -> {args.output}")

    elif args.command == "watch":
        obs = XaraObserver(bridge)
        obs.start(args.duration)
        try:
            while obs.running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            obs.stop()

if __name__ == "__main__":
    main()
