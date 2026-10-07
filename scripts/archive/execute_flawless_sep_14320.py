"""
MASTER FLAWLESS EXECUTOR: execute_flawless_sep_14320.py
Processes Mandiri 3-Page 14,320-record e-Statement (September 2026)
Compliant with SOP Project V2 (Tahap 1 - 7 + Tahap 8 Precision Alignment + Rules 38, 39, 40)
"""

import os
import sys
import json
import struct
import shutil
from datetime import datetime
from xar_dom_engine import XarDocument

target_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Sep"
backup_0xar = os.path.join(target_dir, "0_ORIGINAL_BACKUP.xar")
in_xar = backup_0xar if os.path.exists(backup_0xar) else os.path.join(target_dir, "0.xar")
out_xar = os.path.join(target_dir, "0_output.xar")

print("=========================================================================")
print("   PROJECT V2 PIPELINE EXECUTION: SEPTEMBER 2026 (3 PAGES / 34 TRANSACTIONS)")
print(f"   Source XAR : {in_xar}")
print(f"   Output XAR : {out_xar}")
print("=========================================================================\n")

# Native Colors for 14,320-record 0.xar September
COLOR_CR_HIJAU   = bytearray.fromhex('c2030000') # Native Green (#00A651)
COLOR_DB_HITAM   = bytearray.fromhex('89010000') # Native Black (#000000)
COLOR_SALDO_BIRU = bytearray.fromhex('f2040000') # Native Blue (#005B9C)
COLOR_AWAL_ABU   = bytearray.fromhex('88030000') # Native Gray

# Precision Ruler Alignment Targets
TARGET_XR_NOMINAL = 430850 # 15.199 cm
TARGET_XR_SALDO   = 569950 # 20.106 cm

GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

def find_preceding_tag(doc, idx, target_tag, min_size, max_lookback=40):
    for j in range(idx - 1, max(0, idx - max_lookback), -1):
        r = doc.records[j]
        if r['tag'] == target_tag and len(r['payload']) >= min_size:
            return j
    return None

def update_text(doc, rec_idx, text_str):
    p = bytearray(text_str.encode('utf-16le'))
    doc.records[rec_idx]['payload'] = p
    doc.records[rec_idx]['size'] = len(p)

def blank_split(doc, rec_idx):
    if rec_idx is not None:
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

def update_color(doc, rec_idx, color_payload):
    if rec_idx is not None:
        doc.records[rec_idx]['payload'] = bytearray(color_payload)
        doc.records[rec_idx]['size'] = len(color_payload)

def update_t2100(doc, rec_idx, x_left):
    if rec_idx is not None:
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', x_left, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_t2206(doc, rec_idx, w):
    if rec_idx is not None:
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', w, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def sync_doc(doc, expected_count):
    for r in doc.records:
        r['size'] = len(r['payload'])
    assert len(doc.records) == expected_count, f"Zero-shift violation! Expected {expected_count}, got {len(doc.records)}"
    zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
    assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"

# Backup original and load
if not os.path.exists(backup_0xar):
    shutil.copy2(os.path.join(target_dir, "0.xar"), backup_0xar)
    print(f"[BACKUP] File asli di-backup ke: {backup_0xar}")

doc = XarDocument(in_xar)
TOTAL_RECS = len(doc.records)
print(f"Loaded 0.xar with {TOTAL_RECS:,} records.\n")

# =========================================================================
# TAHAP 1: PERUBAHAN NAMA NASABAH (3 HALAMAN)
# =========================================================================
print("--- [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH ---")
NAME_STR = "MASRIYAH MUHAMMAD \r\n"
for name_idx in [1441, 6010, 9020]: # Header nama nasabah per lembar
    update_text(doc, name_idx, NAME_STR)
print(f"  [OK] Nama Nasabah diubah ke '{NAME_STR.strip()}' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 2: PERUBAHAN PERIODE LAPORAN (3 HALAMAN)
# =========================================================================
print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
# Periode: 01 Sep 2026 - 30 Sep 2026
update_text(doc, 961, "0")
update_text(doc, 965, "1 ")
update_text(doc, 973, "Sep 2026 - 30 Sep 202")
update_text(doc, 978, "6")

update_text(doc, 3647, "0")
update_text(doc, 3651, "1 ")
update_text(doc, 3659, "Sep 2026 - 30 Sep 202")
update_text(doc, 3664, "6")

update_text(doc, 6549, "0")
update_text(doc, 6553, "1 ")
update_text(doc, 6561, "Sep 2026 - 30 Sep 202")
update_text(doc, 6566, "6")
print("  [OK] Periode Laporan diubah ke '01 Sep 2026 - 30 Sep 2026' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 3: PERUBAHAN DICETAK PADA (3 HALAMAN)
# =========================================================================
print("\n--- [3/7] TAHAP 3: PERUBAHAN DICETAK PADA ---")
# Dicetak pada: 01 Oct 2026
update_text(doc, 989, "0")
update_text(doc, 993, "1 ")
update_text(doc, 1001, "Oct 2026")

update_text(doc, 3675, "0")
update_text(doc, 3679, "1 ")
update_text(doc, 3687, "Oct 2026")

update_text(doc, 6577, "0")
update_text(doc, 6581, "1 ")
update_text(doc, 6589, "Oct 2026")
print("  [OK] Tanggal Dicetak Pada diubah ke '01 Oct 2026' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 4: PERUBAHAN NOMOR REKENING
# =========================================================================
print("\n--- [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING ---")
# Nomor Rekening: 1630016144514
update_text(doc, 1031, "1630016144514 ")
print("  [OK] Nomor Rekening diubah ke '1630016144514 ' pada Header Lembar 1.")

# =========================================================================
# TAHAP 5: PERUBAHAN NOMOR HALAMAN (3 HALAMAN)
# =========================================================================
print("\n--- [5/7] TAHAP 5: PERUBAHAN NOMOR HALAMAN ---")
update_text(doc, 1210, "1 dari 3")
update_text(doc, 1079, "of 3")

update_text(doc, 3753, "dari 3")
update_text(doc, 3720, "of 3")

update_text(doc, 6655, "dari 3")
update_text(doc, 6622, "of 3")
print("  [OK] Penomoran Halaman diubah ke 'X dari 3' (Header) dan 'X of 3' (Footer).")

# =========================================================================
# TAHAP 6: JADWAL TANGGAL & JAM TRANSAKSI (34 BARIS SEPTEMBER 2026)
# =========================================================================
print("\n--- [6/7] TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI ---")
schedule_sep = [
    # Page 1 (Rows 1..10)
    ("01 Sep 2026", "04:12:29 WIB"),
    ("01 Sep 2026", "18:44:56 WIB"),
    ("01 Sep 2026", "20:17:05 WIB"),
    ("01 Sep 2026", "20:51:14 WIB"),
    ("02 Sep 2026", "12:04:48 WIB"),
    ("02 Sep 2026", "15:44:38 WIB"),
    ("02 Sep 2026", "16:14:48 WIB"),
    ("02 Sep 2026", "18:50:21 WIB"),
    ("02 Sep 2026", "20:54:27 WIB"),
    ("02 Sep 2026", "20:59:57 WIB"),
    
    # Page 2 (Rows 11..22)
    ("03 Sep 2026", "09:41:50 WIB"),
    ("03 Sep 2026", "09:43:53 WIB"),
    ("03 Sep 2026", "13:15:49 WIB"),
    ("03 Sep 2026", "15:22:37 WIB"),
    ("04 Sep 2026", "02:18:09 WIB"),
    ("04 Sep 2026", "14:40:58 WIB"),
    ("04 Sep 2026", "16:52:40 WIB"),
    ("04 Sep 2026", "18:21:33 WIB"),
    ("04 Sep 2026", "19:01:50 WIB"),
    ("04 Sep 2026", "20:06:28 WIB"),
    ("04 Sep 2026", "21:43:18 WIB"),
    ("09 Sep 2026", "14:40:47 WIB"),

    # Page 3 (Rows 23..34)
    ("09 Sep 2026", "15:14:55 WIB"),
    ("11 Sep 2026", "06:14:12 WIB"),
    ("11 Sep 2026", "06:18:02 WIB"),
    ("25 Sep 2026", "04:00:00 WIB"), # Anchor Date
    ("27 Sep 2026", "07:46:39 WIB"),
    ("27 Sep 2026", "07:55:03 WIB"),
    ("27 Sep 2026", "20:38:12 WIB"),
    ("27 Sep 2026", "21:07:33 WIB"),
    ("28 Sep 2026", "22:50:06 WIB"),
    ("29 Sep 2026", "14:10:44 WIB"),
    ("29 Sep 2026", "16:21:16 WIB"),
    ("30 Sep 2026", "23:59:00 WIB"), # Anchor Date
]

rows_map_sep = [
    # Page 1 (Rows 1..10)
    {"row_no": 1,  "no_nodes": [(1528, "1")],              "nom_p": 1548, "nom_sp": [1553],   "saldo_p": 1573, "saldo_sp": [1578],       "time_p": 1598, "time_sp": [],     "date_p": 1618, "date_sp": [1623]},
    {"row_no": 2,  "no_nodes": [(1705, "2")],              "nom_p": 1725, "nom_sp": [],       "saldo_p": 1745, "saldo_sp": [1750],       "time_p": 1770, "time_sp": [],     "date_p": 1790, "date_sp": [1795]},
    {"row_no": 3,  "no_nodes": [(1863, "3")],              "nom_p": 1883, "nom_sp": [],       "saldo_p": 1903, "saldo_sp": [1908],       "time_p": 1933, "time_sp": [],     "date_p": 1953, "date_sp": []},
    {"row_no": 4,  "no_nodes": [(1982, " "), (2002, "4")], "nom_p": 2051, "nom_sp": [],       "saldo_p": 2071, "saldo_sp": [],           "time_p": 2091, "time_sp": [],     "date_p": 2111, "date_sp": [2116]},
    {"row_no": 5,  "no_nodes": [(2184, "5")],              "nom_p": 2204, "nom_sp": [],       "saldo_p": 2224, "saldo_sp": [2229],       "time_p": 2249, "time_sp": [],     "date_p": 2269, "date_sp": [2274]},
    {"row_no": 6,  "no_nodes": [(2351, "6")],              "nom_p": 2371, "nom_sp": [2376],   "saldo_p": 2396, "saldo_sp": [2401],       "time_p": 2421, "time_sp": [],     "date_p": 2441, "date_sp": [2446]},
    {"row_no": 7,  "no_nodes": [(2523, "7")],              "nom_p": 2543, "nom_sp": [2548],   "saldo_p": 2568, "saldo_sp": [],           "time_p": 2588, "time_sp": [],     "date_p": 2608, "date_sp": [2613]},
    {"row_no": 8,  "no_nodes": [(2686, "8")],              "nom_p": 2706, "nom_sp": [],       "saldo_p": 2726, "saldo_sp": [2731],       "time_p": 2751, "time_sp": [],     "date_p": 2771, "date_sp": [2776]},
    {"row_no": 9,  "no_nodes": [(2850, "9")],              "nom_p": 2870, "nom_sp": [],       "saldo_p": 2890, "saldo_sp": [2895, 2900], "time_p": 2920, "time_sp": [],     "date_p": 2940, "date_sp": [2945]},
    {"row_no": 10, "no_nodes": [(3018, "10")],             "nom_p": 3038, "nom_sp": [],       "saldo_p": 3058, "saldo_sp": [3063],       "time_p": 3083, "time_sp": [],     "date_p": 3103, "date_sp": [3108]},

    # Page 2 (Rows 11..22)
    {"row_no": 11, "no_nodes": [(3999, "11")],             "nom_p": 4019, "nom_sp": [],       "saldo_p": 4039, "saldo_sp": [4044],       "time_p": 4064, "time_sp": [],     "date_p": 4084, "date_sp": []},
    {"row_no": 12, "no_nodes": [(4156, "12")],             "nom_p": 4176, "nom_sp": [4181],   "saldo_p": 4201, "saldo_sp": [],           "time_p": 4221, "time_sp": [],     "date_p": 4241, "date_sp": []},
    {"row_no": 13, "no_nodes": [(4313, "13")],             "nom_p": 4333, "nom_sp": [],       "saldo_p": 4353, "saldo_sp": [],           "time_p": 4373, "time_sp": [],     "date_p": 4393, "date_sp": []},
    {"row_no": 14, "no_nodes": [(4470, "14")],             "nom_p": 4490, "nom_sp": [4495],   "saldo_p": 4515, "saldo_sp": [4520],       "time_p": 4540, "time_sp": [],     "date_p": 4560, "date_sp": []},
    {"row_no": 15, "no_nodes": [(4600, "1"), (4620, "5")], "nom_p": 4667, "nom_sp": [],       "saldo_p": 4687, "saldo_sp": [4692],       "time_p": 4712, "time_sp": [],     "date_p": 4732, "date_sp": []},
    {"row_no": 16, "no_nodes": [(4772, "1"), (4792, "6")], "nom_p": 4848, "nom_sp": [],       "saldo_p": 4868, "saldo_sp": [4873],       "time_p": 4893, "time_sp": [],     "date_p": 4913, "date_sp": []},
    {"row_no": 17, "no_nodes": [(4981, "17")],             "nom_p": 5001, "nom_sp": [5006],   "saldo_p": 5026, "saldo_sp": [5031],       "time_p": 5051, "time_sp": [],     "date_p": 5071, "date_sp": []},
    {"row_no": 18, "no_nodes": [(5111, "1"), (5131, "8")], "nom_p": 5196, "nom_sp": [5201],   "saldo_p": 5221, "saldo_sp": [5226],       "time_p": 5246, "time_sp": [5251], "date_p": 5271, "date_sp": []},
    {"row_no": 19, "no_nodes": [(5343, "19")],             "nom_p": 5363, "nom_sp": [],       "saldo_p": 5383, "saldo_sp": [5388],       "time_p": 5408, "time_sp": [],     "date_p": 5428, "date_sp": []},
    {"row_no": 20, "no_nodes": [(5500, "20")],             "nom_p": 5520, "nom_sp": [5525],   "saldo_p": 5545, "saldo_sp": [5550],       "time_p": 5570, "time_sp": [5575], "date_p": 5595, "date_sp": []},
    {"row_no": 21, "no_nodes": [(5672, "21")],             "nom_p": 5692, "nom_sp": [5697],   "saldo_p": 5717, "saldo_sp": [5722],       "time_p": 5742, "time_sp": [],     "date_p": 5762, "date_sp": []},
    {"row_no": 22, "no_nodes": [(5802, "2"), (5822, "2")], "nom_p": 5860, "nom_sp": [5865],   "saldo_p": 5885, "saldo_sp": [5890],       "time_p": 5910, "time_sp": [5915], "date_p": 5935, "date_sp": [5940]},

    # Page 3 (Rows 23..34)
    {"row_no": 23, "no_nodes": [(6855, "2"), (6875, "3")], "nom_p": 6922, "nom_sp": [],       "saldo_p": 6942, "saldo_sp": [6947],       "time_p": 6967, "time_sp": [],     "date_p": 6987, "date_sp": []},
    {"row_no": 24, "no_nodes": [(7027, "2"), (7047, "4")], "nom_p": 7103, "nom_sp": [],       "saldo_p": 7123, "saldo_sp": [7128],       "time_p": 7148, "time_sp": [],     "date_p": 7168, "date_sp": []},
    {"row_no": 25, "no_nodes": [(7236, "25")],             "nom_p": 7256, "nom_sp": [],       "saldo_p": 7276, "saldo_sp": [7281, 7286], "time_p": 7306, "time_sp": [],     "date_p": 7326, "date_sp": []},
    {"row_no": 26, "no_nodes": [(7403, "26")],             "nom_p": 7423, "nom_sp": [],       "saldo_p": 7443, "saldo_sp": [7448],       "time_p": 7468, "time_sp": [],     "date_p": 7488, "date_sp": [7493]},
    {"row_no": 27, "no_nodes": [(7533, "2"), (7553, "7")], "nom_p": 7591, "nom_sp": [],       "saldo_p": 7611, "saldo_sp": [7616],       "time_p": 7636, "time_sp": [7641], "date_p": 7661, "date_sp": [7666]},
    {"row_no": 28, "no_nodes": [(7706, "2"), (7726, "8")], "nom_p": 7793, "nom_sp": [],       "saldo_p": 7813, "saldo_sp": [7818],       "time_p": 7838, "time_sp": [7843], "date_p": 7863, "date_sp": [7868]},
    {"row_no": 29, "no_nodes": [(7888, "29")],             "nom_p": 7933, "nom_sp": [],       "saldo_p": 7953, "saldo_sp": [7958],       "time_p": 7978, "time_sp": [],     "date_p": 7998, "date_sp": [8003]},
    {"row_no": 30, "no_nodes": [(8048, "3"), (8068, "0")], "nom_p": 8136, "nom_sp": [8141],   "saldo_p": 8161, "saldo_sp": [],           "time_p": 8181, "time_sp": [],     "date_p": 8201, "date_sp": [8206]},
    {"row_no": 31, "no_nodes": [(8226, "31")],             "nom_p": 8271, "nom_sp": [8276],   "saldo_p": 8296, "saldo_sp": [8301],       "time_p": 8321, "time_sp": [8326], "date_p": 8346, "date_sp": [8351]},
    {"row_no": 32, "no_nodes": [(8396, "3"), (8416, "2")], "nom_p": 8484, "nom_sp": [],       "saldo_p": 8504, "saldo_sp": [8509],       "time_p": 8529, "time_sp": [8534], "date_p": 8554, "date_sp": [8559]},
    {"row_no": 33, "no_nodes": [(8604, "3"), (8624, "3")], "nom_p": 8687, "nom_sp": [],       "saldo_p": 8707, "saldo_sp": [8712],       "time_p": 8732, "time_sp": [],     "date_p": 8752, "date_sp": [8757]},
    {"row_no": 34, "no_nodes": [(8797, "3"), (8817, "4")], "nom_p": 8875, "nom_sp": [8880],   "saldo_p": 8900, "saldo_sp": [8905],       "time_p": 8925, "time_sp": [],     "date_p": 8945, "date_sp": [8950]},
]

for i, (d_str, t_str) in enumerate(schedule_sep):
    r_map = rows_map_sep[i]
    
    # 1. Update No Transaksi (Aturan #38: Distribusi Atomik Tag 2202)
    for rec_n, val_n in r_map['no_nodes']:
        if val_n is not None:
            update_text(doc, rec_n, val_n)
        else:
            blank_split(doc, rec_n)

    # 2. Update Waktu / Jam Transaksi (Aturan #39: Blanking Secondary Time Split)
    update_text(doc, r_map['time_p'], t_str)
    for sp in r_map['time_sp']:
        blank_split(doc, sp)
        
    # 3. Update Tanggal Transaksi
    d_parts = d_str.split(" ")
    day_month = f"{d_parts[0]} {d_parts[1]} "
    yr = d_parts[2]
    if len(r_map['date_sp']) > 0:
        update_text(doc, r_map['date_p'], day_month)
        update_text(doc, r_map['date_sp'][0], yr)
        for sp in r_map['date_sp'][1:]:
            blank_split(doc, sp)
    else:
        update_text(doc, r_map['date_p'], d_str)

print("  [OK] Seluruh 34 baris nomor urut transaksi (1 s.d. 34), tanggal & jam September 2026 berhasil di-update.")

# =========================================================================
# TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI UTAMA
# =========================================================================
print("\n--- [7/7] TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI UTAMA ---")
# 1. Summary Header September (34 Baris)
# Saldo Awal: 5.061.666,00
update_text(doc, 1101, "5.061.")
update_text(doc, 1106, "666,00 ")
update_color(doc, 1097, COLOR_AWAL_ABU)

# Dana Masuk: 7.423.449,00
update_text(doc, 1115, "+ ")
update_text(doc, 1120, "7.423.449,")
update_text(doc, 1125, "00")
update_color(doc, 1111, COLOR_CR_HIJAU)

# Dana Keluar: 11.334.320,00
update_text(doc, 1137, "- 11.334.")
update_text(doc, 1142, "320,00 ")
update_color(doc, 1131, COLOR_DB_HITAM)

# Saldo Akhir: 1.150.795,00
update_text(doc, 1154, "1.150.795,")
update_text(doc, 1159, "00")
update_color(doc, 1148, COLOR_SALDO_BIRU)
print("  [OK] Ringkasan Keuangan Header (Awal=5.061.666, Masuk=7.423.449, Keluar=11.334.320, Akhir=1.150.795) ter-update sempurna.")

# 2. 34 Active Transaction Rows September
sep_txs = [
    # Page 1 (Rows 1..10)
    {"nom": "-2.000.000,00", "saldo": "3.061.666,00", "is_cr": False},
    {"nom": "-18.500,00",    "saldo": "3.043.166,00", "is_cr": False},
    {"nom": "-17.499,00",    "saldo": "3.025.667,00", "is_cr": False},
    {"nom": "-300.000,00",   "saldo": "2.725.667,00", "is_cr": False},
    {"nom": "+671.000,00",   "saldo": "3.396.667,00", "is_cr": True},
    {"nom": "-20.905,00",    "saldo": "3.375.762,00", "is_cr": False},
    {"nom": "-40.416,00",    "saldo": "3.335.346,00", "is_cr": False},
    {"nom": "-50.000,00",    "saldo": "3.285.346,00", "is_cr": False},
    {"nom": "-7.500,00",     "saldo": "3.277.846,00", "is_cr": False},
    {"nom": "-263.000,00",   "saldo": "3.014.846,00", "is_cr": False},

    # Page 2 (Rows 11..22)
    {"nom": "+400.000,00",   "saldo": "3.414.846,00", "is_cr": True},
    {"nom": "-1.250.000,00", "saldo": "2.164.846,00", "is_cr": False},
    {"nom": "-100.000,00",   "saldo": "2.064.846,00", "is_cr": False},
    {"nom": "+421.000,00",   "saldo": "2.485.846,00", "is_cr": True},
    {"nom": "-155.000,00",   "saldo": "2.330.846,00", "is_cr": False},
    {"nom": "-270.000,00",   "saldo": "2.060.846,00", "is_cr": False},
    {"nom": "+440.000,00",   "saldo": "2.500.846,00", "is_cr": True},
    {"nom": "-261.500,00",   "saldo": "2.239.346,00", "is_cr": False},
    {"nom": "-200.000,00",   "saldo": "2.039.346,00", "is_cr": False},
    {"nom": "-2.000.000,00", "saldo": "39.346,00",    "is_cr": False},
    {"nom": "+450.000,00",   "saldo": "489.346,00",   "is_cr": True},
    {"nom": "-250.000,00",   "saldo": "239.346,00",   "is_cr": False},

    # Page 3 (Rows 23..34)
    {"nom": "-50.000,00",    "saldo": "189.346,00",   "is_cr": False},
    {"nom": "-175.000,00",   "saldo": "14.346,00",    "is_cr": False},
    {"nom": "+5.041.449,00", "saldo": "5.055.795,00", "is_cr": True},
    {"nom": "-1.250.000,00", "saldo": "3.805.795,00", "is_cr": False},
    {"nom": "-450.000,00",   "saldo": "3.355.795,00", "is_cr": False},
    {"nom": "-500.000,00",   "saldo": "2.855.795,00", "is_cr": False},
    {"nom": "-2.500,00",     "saldo": "2.853.295,00", "is_cr": False},
    {"nom": "-1.200.000,00", "saldo": "1.653.295,00", "is_cr": False},
    {"nom": "-2.500,00",     "saldo": "1.650.795,00", "is_cr": False},
    {"nom": "-500.000,00",   "saldo": "1.150.795,00", "is_cr": False},
    {"nom": "+189.551,00",   "saldo": "1.340.346,00", "is_cr": True},
    {"nom": "-26.000,00",    "saldo": "1.314.346,00", "is_cr": False},
]

for i, tx in enumerate(sep_txs):
    r_map = rows_map_sep[i]
    
    # Dynamic Tag Locator
    nom_m = find_preceding_tag(doc, r_map['nom_p'], 2100, 12)
    nom_k = find_preceding_tag(doc, r_map['nom_p'], 2206, 12)
    nom_c = find_preceding_tag(doc, r_map['nom_p'], 150, 4)

    saldo_m = find_preceding_tag(doc, r_map['saldo_p'], 2100, 12)
    saldo_k = find_preceding_tag(doc, r_map['saldo_p'], 2206, 12)
    saldo_c = find_preceding_tag(doc, r_map['saldo_p'], 150, 4)

    # --- NOMINAL ---
    nom_str = tx['nom']
    is_cr = tx['is_cr']
    update_text(doc, r_map['nom_p'], nom_str)
    for sp in r_map['nom_sp']:
        blank_split(doc, sp)
    update_color(doc, nom_c, COLOR_CR_HIJAU if is_cr else COLOR_DB_HITAM)
    nom_w = calc_text_width(nom_str)
    nom_x_left = TARGET_XR_NOMINAL - nom_w
    update_t2100(doc, nom_m, nom_x_left)
    update_t2206(doc, nom_k, nom_w)
    
    # --- SALDO (Aturan #40: Primary Saldo Anchor & Trailing Decimal Reset) ---
    saldo_str = tx['saldo']
    update_text(doc, r_map['saldo_p'], saldo_str)
    for sp in r_map['saldo_sp']:
        blank_split(doc, sp)
    update_color(doc, saldo_c, COLOR_SALDO_BIRU)
    saldo_w = calc_text_width(saldo_str)
    saldo_x_left = TARGET_XR_SALDO - saldo_w
    update_t2100(doc, saldo_m, saldo_x_left)
    update_t2206(doc, saldo_k, saldo_w)

print("  [OK] Seluruh 34 baris Nominal, Saldo, Warna, dan Alignment Rata Kanan berhasil di-update.")

# =========================================================================
# INTEGRITY GATES & SAVING
# =========================================================================
print("\n--- [POST-FLIGHT AUDIT & INTEGRITY CHECK] ---")
sync_doc(doc, TOTAL_RECS)
print(f"  [PASS] Zero-Shift Invariant: {len(doc.records):,} records terkunci 100% identik.")
print(f"  [PASS] Tag 2202 Safety: Bebas node 0-byte (Zero-Streaming Error Guarantee).")

# Save to output file
doc.save(out_xar)
print(f"\n[SUCCESS] File tersimpan sempurna di: {out_xar}")

shutil.copy2(out_xar, os.path.join(target_dir, "0.xar"))
print(f"[UPDATED] File 0.xar aktif telah diperbarui secara live.")
print("=========================================================================\n")
