"""
MASTER FLAWLESS EXECUTOR: execute_flawless_aug_10429.py
Processes Mandiri 3-Page 10,429-record e-Statement (Aug 2026)
Compliant with SOP Project V2 (Tahap 1 - 7 + Tahap 8 Precision Alignment)
"""

import os
import sys
import json
import struct
import shutil
from datetime import datetime
from xar_dom_engine import XarDocument

target_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug"
backup_0xar = os.path.join(target_dir, "0_ORIGINAL_BACKUP.xar")
in_xar = backup_0xar if os.path.exists(backup_0xar) else os.path.join(target_dir, "0.xar")
out_xar = os.path.join(target_dir, "0_output.xar")

print("=========================================================================")
print("   PROJECT V2 PIPELINE EXECUTION: AGUSTUS 2026 (3 PAGES / 34 TRANSACTIONS)")
print(f"   Source XAR : {in_xar}")
print(f"   Output XAR : {out_xar}")
print("=========================================================================\n")

# Native Colors for 10,429-record 0.xar
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

# Load base document
doc = XarDocument(in_xar)
TOTAL_RECS = len(doc.records)
print(f"Loaded 0.xar with {TOTAL_RECS:,} records.\n")

# =========================================================================
# TAHAP 1: PERUBAHAN NAMA NASABAH (3 HALAMAN)
# =========================================================================
print("--- [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH ---")
NAME_STR = "MASRIYAH MUHAMMAD \r\n"
for name_idx in [1441, 6030, 8858]:
    update_text(doc, name_idx, NAME_STR)
print(f"  [OK] Nama Nasabah diubah ke '{NAME_STR.strip()}' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 2: PERUBAHAN PERIODE LAPORAN (3 HALAMAN)
# =========================================================================
print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
# Periode: 01 Aug 2026 - 31 Aug 2026
update_text(doc, 961, "0")
update_text(doc, 965, "1 ")
update_text(doc, 973, "Aug 2026 - 31 Aug 202")
update_text(doc, 978, "6")

update_text(doc, 3682, "0")
update_text(doc, 3686, "1 ")
update_text(doc, 3694, "Aug 2026 - 31 Aug 202")
update_text(doc, 3699, "6")

update_text(doc, 6569, "0")
update_text(doc, 6573, "1 ")
update_text(doc, 6581, "Aug 2026 - 31 Aug 202")
update_text(doc, 6586, "6")
print("  [OK] Periode Laporan diubah ke '01 Aug 2026 - 31 Aug 2026' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 3: PERUBAHAN DICETAK PADA (3 HALAMAN)
# =========================================================================
print("\n--- [3/7] TAHAP 3: PERUBAHAN DICETAK PADA ---")
# Dicetak pada: 01 Oct 2026
update_text(doc, 989, "0")
update_text(doc, 993, "1 ")
update_text(doc, 1001, "Oct 2026")

update_text(doc, 3710, "0")
update_text(doc, 3714, "1 ")
update_text(doc, 3722, "Oct 2026")

update_text(doc, 6597, "0")
update_text(doc, 6601, "1 ")
update_text(doc, 6609, "Oct 2026")
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

update_text(doc, 3788, "dari 3")
update_text(doc, 3755, "of 3")

update_text(doc, 6675, "dari 3")
update_text(doc, 6642, "of 3")
print("  [OK] Penomoran Halaman diubah ke 'X dari 3' (Header) dan 'X of 3' (Footer).")

# =========================================================================
# TAHAP 6: JADWAL TANGGAL & JAM TRANSAKSI (34 BARIS AGUSTUS 2026)
# =========================================================================
print("\n--- [6/7] TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI ---")
schedule_aug = [
    # Page 1 (Rows 1..10)
    ("01 Aug 2026", "04:12:29 WIB"),
    ("01 Aug 2026", "18:44:56 WIB"),
    ("01 Aug 2026", "20:17:05 WIB"),
    ("01 Aug 2026", "20:51:14 WIB"),
    ("05 Aug 2026", "12:04:48 WIB"),
    ("05 Aug 2026", "15:44:38 WIB"),
    ("05 Aug 2026", "16:14:48 WIB"),
    ("05 Aug 2026", "18:50:21 WIB"),
    ("05 Aug 2026", "20:54:27 WIB"),
    ("05 Aug 2026", "20:59:57 WIB"),
    
    # Page 2 (Rows 11..22)
    ("10 Aug 2026", "09:41:50 WIB"),
    ("10 Aug 2026", "09:43:53 WIB"),
    ("10 Aug 2026", "13:15:49 WIB"),
    ("10 Aug 2026", "15:22:37 WIB"),
    ("17 Aug 2026", "12:18:09 WIB"),
    ("17 Aug 2026", "14:40:58 WIB"),
    ("17 Aug 2026", "16:52:40 WIB"),
    ("17 Aug 2026", "18:21:33 WIB"),
    ("17 Aug 2026", "19:01:50 WIB"),
    ("17 Aug 2026", "20:06:28 WIB"),
    ("17 Aug 2026", "21:43:18 WIB"),
    ("22 Aug 2026", "14:40:47 WIB"),

    # Page 3 (Rows 23..34)
    ("22 Aug 2026", "15:14:55 WIB"),
    ("24 Aug 2026", "06:14:12 WIB"),
    ("24 Aug 2026", "06:18:02 WIB"),
    ("25 Aug 2026", "04:00:00 WIB"), # Anchor Date
    ("27 Aug 2026", "07:46:39 WIB"),
    ("27 Aug 2026", "07:55:03 WIB"),
    ("27 Aug 2026", "20:38:12 WIB"),
    ("27 Aug 2026", "21:07:33 WIB"),
    ("28 Aug 2026", "22:50:06 WIB"),
    ("29 Aug 2026", "14:10:44 WIB"),
    ("29 Aug 2026", "16:21:16 WIB"),
    ("31 Aug 2026", "23:59:00 WIB"), # Anchor Date
]

rows_map_aug = [
    # Page 1 (Rows 1..10)
    {"row_no": 1,  "no_nodes": [(1509, "1")],              "nom_p": 1529, "nom_sp": [],     "saldo_p": 1549, "saldo_sp": [],       "time_p": 1569, "time_sp": [], "date_p": 1589, "date_sp": [1594]},
    {"row_no": 2,  "no_nodes": [(1666, "2")],              "nom_p": 1686, "nom_sp": [],     "saldo_p": 1706, "saldo_sp": [1711],   "time_p": 1731, "time_sp": [], "date_p": 1751, "date_sp": [1756]},
    {"row_no": 3,  "no_nodes": [(1824, "3")],              "nom_p": 1844, "nom_sp": [],     "saldo_p": 1864, "saldo_sp": [1869],   "time_p": 1889, "time_sp": [], "date_p": 1909, "date_sp": [1914]},
    {"row_no": 4,  "no_nodes": [(1954, " "), (1974, "4")], "nom_p": 2021, "nom_sp": [],     "saldo_p": 2041, "saldo_sp": [2046],   "time_p": 2066, "time_sp": [], "date_p": 2086, "date_sp": [2091]},
    {"row_no": 5,  "no_nodes": [(2131, " "), (2151, "5")], "nom_p": 2198, "nom_sp": [],     "saldo_p": 2218, "saldo_sp": [2223],   "time_p": 2243, "time_sp": [], "date_p": 2263, "date_sp": [2268]},
    {"row_no": 6,  "no_nodes": [(2367, "6")],              "nom_p": 2387, "nom_sp": [2392], "saldo_p": 2412, "saldo_sp": [],       "time_p": 2432, "time_sp": [], "date_p": 2452, "date_sp": []},
    {"row_no": 7,  "no_nodes": [(2524, "7")],              "nom_p": 2544, "nom_sp": [2549], "saldo_p": 2569, "saldo_sp": [2574],   "time_p": 2594, "time_sp": [], "date_p": 2614, "date_sp": []},
    {"row_no": 8,  "no_nodes": [(2711, "8")],              "nom_p": 2731, "nom_sp": [],     "saldo_p": 2751, "saldo_sp": [2756],   "time_p": 2776, "time_sp": [], "date_p": 2796, "date_sp": []},
    {"row_no": 9,  "no_nodes": [(2868, "9")],              "nom_p": 2888, "nom_sp": [],     "saldo_p": 2908, "saldo_sp": [2913],   "time_p": 2933, "time_sp": [], "date_p": 2953, "date_sp": []},
    {"row_no": 10, "no_nodes": [(3058, "10")],             "nom_p": 3078, "nom_sp": [3083], "saldo_p": 3103, "saldo_sp": [],       "time_p": 3123, "time_sp": [], "date_p": 3143, "date_sp": []},

    # Page 2 (Rows 11..22)
    {"row_no": 11, "no_nodes": [(4025, "11")],             "nom_p": 4045, "nom_sp": [4050], "saldo_p": 4070, "saldo_sp": [],       "time_p": 4090, "time_sp": [], "date_p": 4110, "date_sp": []},
    {"row_no": 12, "no_nodes": [(4130, "12")],             "nom_p": 4190, "nom_sp": [],     "saldo_p": 4210, "saldo_sp": [4215],   "time_p": 4235, "time_sp": [], "date_p": 4255, "date_sp": []},
    {"row_no": 13, "no_nodes": [(4295, "1"), (4315, "3")], "nom_p": 4362, "nom_sp": [4367], "saldo_p": 4387, "saldo_sp": [4392],   "time_p": 4412, "time_sp": [4417], "date_p": 4437, "date_sp": []},
    {"row_no": 14, "no_nodes": [(4509, "14")],             "nom_p": 4529, "nom_sp": [],     "saldo_p": 4549, "saldo_sp": [4554],   "time_p": 4574, "time_sp": [4579], "date_p": 4599, "date_sp": []},
    {"row_no": 15, "no_nodes": [(4667, "15")],             "nom_p": 4687, "nom_sp": [],     "saldo_p": 4707, "saldo_sp": [],       "time_p": 4727, "time_sp": [4732], "date_p": 4752, "date_sp": []},
    {"row_no": 16, "no_nodes": [(4824, "16")],             "nom_p": 4844, "nom_sp": [],     "saldo_p": 4864, "saldo_sp": [4869],   "time_p": 4889, "time_sp": [], "date_p": 4909, "date_sp": []},
    {"row_no": 17, "no_nodes": [(4949, "1"), (4969, "7")], "nom_p": 5012, "nom_sp": [],     "saldo_p": 5032, "saldo_sp": [5037],   "time_p": 5057, "time_sp": [5062], "date_p": 5082, "date_sp": []},
    {"row_no": 18, "no_nodes": [(5122, "1"), (5142, "8")], "nom_p": 5185, "nom_sp": [],     "saldo_p": 5205, "saldo_sp": [5210],   "time_p": 5230, "time_sp": [], "date_p": 5250, "date_sp": []},
    {"row_no": 19, "no_nodes": [(5290, "1"), (5310, "9")], "nom_p": 5357, "nom_sp": [],     "saldo_p": 5377, "saldo_sp": [5382],   "time_p": 5402, "time_sp": [5407], "date_p": 5427, "date_sp": []},
    {"row_no": 20, "no_nodes": [(5467, "2"), (5487, "0")], "nom_p": 5534, "nom_sp": [5539], "saldo_p": 5559, "saldo_sp": [5564],   "time_p": 5584, "time_sp": [], "date_p": 5604, "date_sp": [5609]},
    {"row_no": 21, "no_nodes": [(5660, "2"), (5680, "1")], "nom_p": 5732, "nom_sp": [],     "saldo_p": 5752, "saldo_sp": [5757],   "time_p": 5777, "time_sp": [], "date_p": 5797, "date_sp": [5802]},
    {"row_no": 22, "no_nodes": [(5870, "22")],             "nom_p": 5890, "nom_sp": [],     "saldo_p": 5910, "saldo_sp": [5915],   "time_p": 5935, "time_sp": [], "date_p": 5955, "date_sp": [5960]},

    # Page 3 (Rows 23..34)
    {"row_no": 23, "no_nodes": [(6875, "2"), (6895, "3")], "nom_p": 6942, "nom_sp": [],     "saldo_p": 6962, "saldo_sp": [6967],   "time_p": 6987, "time_sp": [], "date_p": 7007, "date_sp": []},
    {"row_no": 24, "no_nodes": [(7075, "24")],             "nom_p": 7095, "nom_sp": [],     "saldo_p": 7115, "saldo_sp": [],       "time_p": 7135, "time_sp": [7140], "date_p": 7160, "date_sp": []},
    {"row_no": 25, "no_nodes": [(7228, "25")],             "nom_p": 7248, "nom_sp": [],     "saldo_p": 7268, "saldo_sp": [7273],   "time_p": 7293, "time_sp": [7298], "date_p": 7318, "date_sp": []},
    {"row_no": 26, "no_nodes": [(7426, "26")],             "nom_p": 7446, "nom_sp": [7451], "saldo_p": 7471, "saldo_sp": [7476],   "time_p": 7496, "time_sp": [], "date_p": 7516, "date_sp": [7521]},
    {"row_no": 27, "no_nodes": [(7584, "27")],             "nom_p": 7604, "nom_sp": [7609], "saldo_p": 7629, "saldo_sp": [7634],   "time_p": 7654, "time_sp": [], "date_p": 7674, "date_sp": []},
    {"row_no": 28, "no_nodes": [(7737, "28")],             "nom_p": 7757, "nom_sp": [],     "saldo_p": 7777, "saldo_sp": [7782],   "time_p": 7802, "time_sp": [], "date_p": 7822, "date_sp": []},
    {"row_no": 29, "no_nodes": [(7862, "2"), (7882, "9")], "nom_p": 7920, "nom_sp": [],     "saldo_p": 7940, "saldo_sp": [7945],   "time_p": 7965, "time_sp": [], "date_p": 7985, "date_sp": []},
    {"row_no": 30, "no_nodes": [(8053, "30")],             "nom_p": 8073, "nom_sp": [8078], "saldo_p": 8098, "saldo_sp": [8103],   "time_p": 8123, "time_sp": [], "date_p": 8143, "date_sp": []},
    {"row_no": 31, "no_nodes": [(8183, "3"), (8203, "1")], "nom_p": 8241, "nom_sp": [],     "saldo_p": 8261, "saldo_sp": [8266],   "time_p": 8286, "time_sp": [], "date_p": 8306, "date_sp": []},
    {"row_no": 32, "no_nodes": [(8378, "32")],             "nom_p": 8398, "nom_sp": [],     "saldo_p": 8418, "saldo_sp": [8423],   "time_p": 8443, "time_sp": [], "date_p": 8463, "date_sp": []},
    {"row_no": 33, "no_nodes": [(8536, "33")],             "nom_p": 8556, "nom_sp": [],     "saldo_p": 8576, "saldo_sp": [8581],   "time_p": 8601, "time_sp": [], "date_p": 8621, "date_sp": []},
    {"row_no": 34, "no_nodes": [(8698, "34")],             "nom_p": 8718, "nom_sp": [],     "saldo_p": 8738, "saldo_sp": [8743],   "time_p": 8763, "time_sp": [], "date_p": 8783, "date_sp": [8788]},
]

for i, (d_str, t_str) in enumerate(schedule_aug):
    r_map = rows_map_aug[i]
    
    # 1. Update No Transaksi (1 s.d. 34)
    for rec_n, val_n in r_map['no_nodes']:
        if val_n is not None:
            update_text(doc, rec_n, val_n)
        else:
            blank_split(doc, rec_n)

    # 2. Update Waktu / Jam Transaksi
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

print("  [OK] Seluruh 34 baris nomor urut transaksi (1 s.d. 34), tanggal & jam Agustus 2026 berhasil di-update.")

# =========================================================================
# TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI UTAMA
# =========================================================================
print("\n--- [7/7] TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI UTAMA ---")
# 1. Summary Header
# Saldo Awal: 270.510,00
update_text(doc, 1101, "270.")
update_text(doc, 1106, "510,00 ")
update_color(doc, 1097, COLOR_AWAL_ABU)

# Dana Masuk: 7.252.349,00
update_text(doc, 1115, "+ ")
update_text(doc, 1120, "7.252.349,")
update_text(doc, 1125, "00")
update_color(doc, 1111, COLOR_CR_HIJAU)

# Dana Keluar: 2.461.193,00
update_text(doc, 1137, "- 2.461.")
update_text(doc, 1142, "193,00 ")
update_color(doc, 1131, COLOR_DB_HITAM)

# Saldo Akhir: 5.061.666,00
update_text(doc, 1154, "5.061.666,")
update_text(doc, 1159, "00")
update_color(doc, 1148, COLOR_SALDO_BIRU)
print("  [OK] Ringkasan Keuangan Header (Awal, Masuk, Keluar, Akhir) ter-update sempurna.")

# 2. 34 Active Transaction Rows
aug_txs = [
    # Page 1 (Rows 1..10)
    {"nom": "-195.707,00", "saldo": "74.803,00", "is_cr": False},
    {"nom": "-49.700,00",  "saldo": "25.103,00", "is_cr": False},
    {"nom": "+400.000,00", "saldo": "425.103,00", "is_cr": True},
    {"nom": "-50.000,00",  "saldo": "375.103,00", "is_cr": False},
    {"nom": "-350.000,00", "saldo": "25.103,00", "is_cr": False},
    {"nom": "+64.400,00",  "saldo": "89.503,00", "is_cr": True},
    {"nom": "-64.500,00",  "saldo": "25.003,00", "is_cr": False},
    {"nom": "+80.000,00",  "saldo": "105.003,00", "is_cr": True},
    {"nom": "-80.003,00",  "saldo": "25.000,00", "is_cr": False},
    {"nom": "+62.819,00",  "saldo": "87.819,00", "is_cr": True},

    # Page 2 (Rows 11..22)
    {"nom": "+200.000,00", "saldo": "287.819,00", "is_cr": True},
    {"nom": "-5.500,00",   "saldo": "282.319,00", "is_cr": False},
    {"nom": "-250.000,00", "saldo": "32.319,00", "is_cr": False},
    {"nom": "+85.000,00",  "saldo": "117.319,00", "is_cr": True},
    {"nom": "-33.000,00",  "saldo": "84.319,00", "is_cr": False},
    {"nom": "-15.000,00",  "saldo": "69.319,00", "is_cr": False},
    {"nom": "-26.000,00",  "saldo": "43.319,00", "is_cr": False},
    {"nom": "+300.000,00", "saldo": "343.319,00", "is_cr": True},
    {"nom": "-13.000,00",  "saldo": "330.319,00", "is_cr": False},
    {"nom": "-305.000,00", "saldo": "25.319,00", "is_cr": False},
    {"nom": "+100.000,00", "saldo": "125.319,00", "is_cr": True},
    {"nom": "+420.000,00", "saldo": "545.319,00", "is_cr": True},

    # Page 3 (Rows 23..34)
    {"nom": "-500.000,00", "saldo": "45.319,00", "is_cr": False},
    {"nom": "-500,00",     "saldo": "44.819,00", "is_cr": False},
    {"nom": "-18.000,00",  "saldo": "26.819,00", "is_cr": False},
    {"nom": "+5.014.630,00", "saldo": "5.041.449,00", "is_cr": True},
    {"nom": "-26.430,00",  "saldo": "5.015.019,00", "is_cr": False},
    {"nom": "-18.853,00",  "saldo": "4.996.166,00", "is_cr": False},
    {"nom": "-280.000,00", "saldo": "4.716.166,00", "is_cr": False},
    {"nom": "+525.500,00", "saldo": "5.241.666,00", "is_cr": True},
    {"nom": "-25.000,00",  "saldo": "5.216.666,00", "is_cr": False},
    {"nom": "-50.000,00",  "saldo": "5.166.666,00", "is_cr": False},
    {"nom": "-100.000,00", "saldo": "5.066.666,00", "is_cr": False},
    {"nom": "-5.000,00",   "saldo": "5.061.666,00", "is_cr": False},
]

for i, tx in enumerate(aug_txs):
    r_map = rows_map_aug[i]
    
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
    
    # --- SALDO ---
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

# Backup original and update live
backup_0xar = os.path.join(target_dir, "0_ORIGINAL_BACKUP.xar")
if not os.path.exists(backup_0xar):
    shutil.copy2(in_xar, backup_0xar)
    print(f"[BACKUP] File asli di-backup ke: {backup_0xar}")

shutil.copy2(out_xar, os.path.join(target_dir, "0.xar"))
print(f"[UPDATED] File 0.xar aktif telah diperbarui secara live.")
print("=========================================================================\n")
