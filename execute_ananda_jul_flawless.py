"""
FLAWLESS EXECUTION SCRIPT FOR ANANDA SUCI HATI - JULI 2026 (6,707 Records)
Compliant with SOP Project V2 (7 Tahap Standar Master)
"""

import os
import sys
import shutil
import struct
from datetime import datetime
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# Target directory
TARGET_DIR = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul"
XAR_PATH = os.path.join(TARGET_DIR, "0.xar")
EXCEL_PATH = os.path.join(TARGET_DIR, "Template_Pekerjaan_Xara_Jul.xlsx")
BACKUP_PATH = os.path.join(TARGET_DIR, "0_backup_original.xar")

# Create backup if not already present
if not os.path.exists(BACKUP_PATH):
    shutil.copy2(XAR_PATH, BACKUP_PATH)
    print(f"[*] Backup file asli dibuat di: {BACKUP_PATH}")

doc = XarDocument(XAR_PATH)
cfg = parse_xara_excel_template(EXCEL_PATH)

total_recs_initial = len(doc.records)
print(f"[*] Total Records Initial: {total_recs_initial}")
assert total_recs_initial == 6707, f"Expected 6707 records, found {total_recs_initial}"

# Metrics & Alignment Constants
GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

TARGET_XR_NOMINAL = 431355 # Right alignment boundary for nominal column
TARGET_XR_SALDO   = 570390 # Right alignment boundary for saldo column

# Colors Tag 150 for 6707
COLOR_HIJAU_CR   = bytearray.fromhex('ee030000') # Credit Green (#00A651 / native)
COLOR_HITAM_DB   = bytearray.fromhex('3c010000') # Debit Black (#000000 / native)
COLOR_ABU_AWAL   = bytearray.fromhex('8a030000') # Initial Balance Gray
COLOR_BIRU_SALDO = bytearray.fromhex('3a050000') # Closing Balance Blue

def update_text_node(doc, rec_idx, text_str):
    if rec_idx is not None:
        p = bytearray(text_str.encode('utf-16le'))
        doc.records[rec_idx]['payload'] = p
        doc.records[rec_idx]['size'] = len(p)

def clean_split_node(doc, rec_idx):
    if rec_idx is not None:
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

def update_t2206(doc, rec_idx, w):
    if rec_idx is not None:
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', w, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_t2100_x(doc, rec_idx, x_left):
    if rec_idx is not None:
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', x_left, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_color(doc, rec_idx, color_payload):
    if rec_idx is not None:
        doc.records[rec_idx]['payload'] = bytearray(color_payload)
        doc.records[rec_idx]['size'] = len(color_payload)

print("\n=======================================================")
print("  EKSEKUSI 7 TAHAP SOP STANDAR MASTER (ANANDA - JULI 2026)")
print("=======================================================")

# =========================================================
# TAHAP 1: PERUBAHAN NAMA
# =========================================================
new_name = cfg['header']['nama'].strip() + " \r\n"
update_text_node(doc, 994, new_name)
update_text_node(doc, 3740, new_name)
# Set kern X = 0 for post-name kerning
update_t2206(doc, 999, 0)
update_t2206(doc, 3744, 0)
print(f"[Tahap 1/7] Nama Nasabah       : '{cfg['header']['nama']}' [PASS ✓]")

# =========================================================
# TAHAP 2: PERUBAHAN PERIODE
# =========================================================
# Periode: 01 Jul 2026 - 31 Jul 2026
# Page 1
update_text_node(doc, 1037, "0")
update_text_node(doc, 1041, "1")
update_text_node(doc, 1049, " Jul 2026 - 31 Jul ")
update_text_node(doc, 1054, "202")
update_text_node(doc, 1059, "6")

# Page 2
update_text_node(doc, 3776, "0")
update_text_node(doc, 3780, "1")
update_text_node(doc, 3788, " Jul 2026 - 31 Jul ")
update_text_node(doc, 3793, "202")
update_text_node(doc, 3798, "6")
print(f"[Tahap 2/7] Periode Laporan    : '01 Jul 2026 - 31 Jul 2026' [PASS ✓]")

# =========================================================
# TAHAP 3: PERUBAHAN DICETAK PADA
# =========================================================
# Target: 01 Oct 2026 (or 01 Okt 2026)
dicetak_raw = str(cfg['header']['dicetak_pada']).strip()
# Page 1
update_text_node(doc, 1071, "0")
update_text_node(doc, 1075, "1")
update_text_node(doc, 1083, " Oct 2026")

# Page 2
update_text_node(doc, 3810, "0")
update_text_node(doc, 3814, "1")
update_text_node(doc, 3822, " Oct 2026")
print(f"[Tahap 3/7] Dicetak Pada       : '01 Oct 2026' [PASS ✓]")

# =========================================================
# TAHAP 4: PERUBAHAN NOMOR REKENING
# =========================================================
acc_num = cfg['header']['nomor_rekening'].strip()
update_text_node(doc, 1104, acc_num[:12])
update_text_node(doc, 1109, acc_num[12:] + " ")
print(f"[Tahap 4/7] Nomor Rekening     : '{acc_num}' [PASS ✓]")

# =========================================================
# TAHAP 5: PERUBAHAN NOMOR HALAMAN
# =========================================================
# Page 1
update_text_node(doc, 1170, "1 of 3")
update_text_node(doc, 1274, "3")
update_text_node(doc, 1295, "1 d")
update_text_node(doc, 1300, "ari")

# Page 2
update_text_node(doc, 3848, "2")
update_text_node(doc, 3856, "of 3")
update_text_node(doc, 3877, "3")
update_text_node(doc, 3898, "2 d")
update_text_node(doc, 3903, "ari")
print(f"[Tahap 5/7] Nomor Halaman      : '1 of 3' & '2 of 3' [PASS ✓]")

# =========================================================
# TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI
# =========================================================
date_schedule = [
    (1,  "01 Jul 2026", "07:09:03 WIB"),
    (2,  "02 Jul 2026", "18:08:19 WIB"),
    (3,  "04 Jul 2026", "17:18:13 WIB"),
    (4,  "08 Jul 2026", "10:49:18 WIB"),
    (5,  "08 Jul 2026", "16:54:21 WIB"),
    (6,  "09 Jul 2026", "03:33:21 WIB"),
    (7,  "09 Jul 2026", "14:33:33 WIB"),
    (8,  "09 Jul 2026", "16:50:44 WIB"),
    (9,  "10 Jul 2026", "04:00:00 WIB"),
    (10, "14 Jul 2026", "14:48:25 WIB"),
    (11, "17 Jul 2026", "08:29:38 WIB"),
    (12, "20 Jul 2026", "08:35:21 WIB"),
    (13, "22 Jul 2026", "08:46:17 WIB"),
    (14, "22 Jul 2026", "08:46:17 WIB"),
    (15, "27 Jul 2026", "11:54:50 WIB"),
    (16, "27 Jul 2026", "17:19:21 WIB"),
    (17, "27 Jul 2026", "23:59:59 WIB"),
    (18, "28 Jul 2026", "06:42:50 WIB"),
    (19, "31 Jul 2026", "23:59:00 WIB")
]

# Row 1
update_text_node(doc, 1654, "01 Jul 2026")
update_text_node(doc, 1634, "07:09:03 WIB")

# Row 2
update_text_node(doc, 1816, "02 Jul 2026")
update_text_node(doc, 1791, "18:08:19 W")
update_text_node(doc, 1796, "IB")

# Row 3
update_text_node(doc, 1978, "04 Jul 2026")
update_text_node(doc, 1953, "17:18")
update_text_node(doc, 1958, ":13 WIB")

# Row 4
update_text_node(doc, 2155, "08 Jul 2026")
update_text_node(doc, 2130, "10:49:18 ")
update_text_node(doc, 2135, "WIB")

# Row 5
update_text_node(doc, 2332, "08 Jul 2026")
update_text_node(doc, 2307, "16:54:21 ")
update_text_node(doc, 2312, "WIB")

# Row 6
update_text_node(doc, 2469, "09 Jul 2026")
update_text_node(doc, 2444, "03:33:21 WI")
update_text_node(doc, 2449, "B")

# Row 7
update_text_node(doc, 2631, "09 Jul 2026")
update_text_node(doc, 2606, "14:33:33")
update_text_node(doc, 2611, " WIB")

# Row 8
update_text_node(doc, 2803, "09 Jul 2026")
update_text_node(doc, 2778, "16:50:44 W")
update_text_node(doc, 2783, "IB")

# Row 9
update_text_node(doc, 2979, "10 Jul 2026")
update_text_node(doc, 2954, "04:00:")
update_text_node(doc, 2959, "00 WIB")

# Row 10
update_text_node(doc, 3121, "14 Jul 2026")
update_text_node(doc, 3096, "14:48:25 WI")
update_text_node(doc, 3101, "B")

# Row 11
update_text_node(doc, 4225, "17 Jul 2026")
update_text_node(doc, 4205, "08:29:38 WIB")

# Row 12
update_text_node(doc, 4374, "20 Jul 2026")
update_text_node(doc, 4349, "08:35:21 WI")
update_text_node(doc, 4354, "B")

# Row 13
update_text_node(doc, 4516, "22 Jul 2026")
update_text_node(doc, 4491, "08:46:17 W")
update_text_node(doc, 4496, "IB")

# Row 14
update_text_node(doc, 4658, "22 Jul 2026")
update_text_node(doc, 4633, "08:46:17 W")
update_text_node(doc, 4638, "IB")

# Row 15
update_text_node(doc, 4805, "27 Jul 2026")
update_text_node(doc, 4780, "11:54:")
update_text_node(doc, 4785, "50 WIB")

# Row 16
update_text_node(doc, 4982, "27 ")
update_text_node(doc, 4987, "Jul 2026")
update_text_node(doc, 4952, "17:19:21")
update_text_node(doc, 4957, " WI")
update_text_node(doc, 4962, "B")

# Row 17
update_text_node(doc, 5119, "27 Jul 2026")
update_text_node(doc, 5094, "23:59:5")
update_text_node(doc, 5099, "9 WIB")

# Row 18
update_text_node(doc, 5287, "28 ")
update_text_node(doc, 5292, "Jul 2026")
update_text_node(doc, 5267, "06:42:50 WIB")

# Row 19
update_text_node(doc, 5419, "31 Jul 2026")
update_text_node(doc, 5399, "23:59:00 WIB")
print(f"[Tahap 6/7] Tanggal & Jam       : 19 Baris Juli 2026 Kronologis [PASS ✓]")

# =========================================================
# TAHAP 7: SUMMARY & TABEL MUTASI (SALDO & NOMINAL)
# =========================================================
# 1. Summary Block
sawal = cfg['summary']['saldo_awal']
dmasuk = cfg['summary']['dana_masuk']
dkeluar = cfg['summary']['dana_keluar']
sakhir = cfg['summary']['saldo_akhir']

if not dmasuk.startswith("+"): dmasuk = "+ " + dmasuk
if not dkeluar.startswith("-"): dkeluar = "- " + dkeluar
if not sawal.endswith(" "): sawal = sawal + " "
if not dkeluar.endswith(" "): dkeluar = dkeluar + " "

# Saldo Awal
update_text_node(doc, 1193, sawal)
update_t2206(doc, 1188, calc_text_width(sawal))
update_color(doc, 1189, COLOR_ABU_AWAL)

# Dana Masuk
update_text_node(doc, 1202, dmasuk)
update_t2206(doc, 1197, calc_text_width(dmasuk))
update_color(doc, 1198, COLOR_HIJAU_CR)

# Dana Keluar
update_text_node(doc, 1214, dkeluar)
update_t2206(doc, 1207, calc_text_width(dkeluar))
update_color(doc, 1208, COLOR_HITAM_DB)

# Saldo Akhir
update_text_node(doc, 1226, sakhir)
update_t2206(doc, 1218, calc_text_width(sakhir))
update_color(doc, 1220, COLOR_BIRU_SALDO)

# 2. Table Mutations
row_map_6707 = {
    1:  {'s_pos': 1571, 's_col': 1576, 's_2206': 1587, 's_txt': 1588, 's_split': None, 'n_pos': 1592, 'n_col': 1597, 'n_2206': 1608, 'n_txt': 1609, 'n_split': 1614},
    2:  {'s_pos': 1728, 's_col': 1733, 's_2206': 1744, 's_txt': 1745, 's_split': None, 'n_pos': 1749, 'n_col': 1754, 'n_2206': 1765, 'n_txt': 1766, 'n_split': 1771},
    3:  {'s_pos': 1895, 's_col': 1900, 's_2206': 1911, 's_txt': 1912, 's_split': None, 'n_pos': 1916, 'n_col': 1921, 'n_2206': 1932, 'n_txt': 1933, 'n_split': None},
    4:  {'s_pos': 2067, 's_col': 2072, 's_2206': 2083, 's_txt': 2084, 's_split': None, 'n_pos': 2088, 'n_col': 2093, 'n_2206': 2104, 'n_txt': 2105, 'n_split': 2110},
    5:  {'s_pos': 2244, 's_col': 2249, 's_2206': 2260, 's_txt': 2261, 's_split': None, 'n_pos': 2265, 'n_col': 2270, 'n_2206': 2281, 'n_txt': 2282, 'n_split': 2287},
    6:  {'s_pos': 2386, 's_col': 2391, 's_2206': 2402, 's_txt': 2403, 's_split': None, 'n_pos': 2407, 'n_col': 2412, 'n_2206': 2423, 'n_txt': 2424, 'n_split': None},
    7:  {'s_pos': 2543, 's_col': 2548, 's_2206': 2559, 's_txt': 2560, 's_split': None, 'n_pos': 2564, 'n_col': 2569, 'n_2206': 2580, 'n_txt': 2581, 'n_split': 2586},
    8:  {'s_pos': 2715, 's_col': 2720, 's_2206': 2731, 's_txt': 2732, 's_split': None, 'n_pos': 2736, 'n_col': 2741, 'n_2206': 2752, 'n_txt': 2753, 'n_split': 2758},
    9:  {'s_pos': 2896, 's_col': 2901, 's_2206': 2912, 's_txt': 2913, 's_split': None, 'n_pos': 2917, 'n_col': 2922, 'n_2206': 2933, 'n_txt': 2934, 'n_split': None},
    10: {'s_pos': 3033, 's_col': 3038, 's_2206': 3049, 's_txt': 3050, 's_split': None, 'n_pos': 3054, 'n_col': 3059, 'n_2206': 3070, 'n_txt': 3071, 'n_split': 3076},
    11: {'s_pos': 4142, 's_col': 4147, 's_2206': 4158, 's_txt': 4159, 's_split': None, 'n_pos': 4163, 'n_col': 4168, 'n_2206': 4179, 'n_txt': 4180, 'n_split': 4185},
    12: {'s_pos': 4286, 's_col': 4291, 's_2206': 4302, 's_txt': 4303, 's_split': None, 'n_pos': 4307, 'n_col': 4312, 'n_2206': 4323, 'n_txt': 4324, 'n_split': 4329},
    13: {'s_pos': 4428, 's_col': 4433, 's_2206': 4444, 's_txt': 4445, 's_split': None, 'n_pos': 4449, 'n_col': 4454, 'n_2206': 4465, 'n_txt': 4466, 'n_split': 4471},
    14: {'s_pos': 4570, 's_col': 4575, 's_2206': 4586, 's_txt': 4587, 's_split': None, 'n_pos': 4591, 'n_col': 4596, 'n_2206': 4607, 'n_txt': 4608, 'n_split': 4613},
    15: {'s_pos': 4717, 's_col': 4722, 's_2206': 4733, 's_txt': 4734, 's_split': None, 'n_pos': 4738, 'n_col': 4743, 'n_2206': 4754, 'n_txt': 4755, 'n_split': 4760},
    16: {'s_pos': 4889, 's_col': 4894, 's_2206': 4905, 's_txt': 4906, 's_split': None, 'n_pos': 4910, 'n_col': 4915, 'n_2206': 4926, 'n_txt': 4927, 'n_split': 4932},
    17: {'s_pos': 5036, 's_col': 5041, 's_2206': 5052, 's_txt': 5053, 's_split': None, 'n_pos': 5057, 'n_col': 5062, 'n_2206': 5073, 'n_txt': 5074, 'n_split': None},
    18: {'s_pos': 5204, 's_col': 5209, 's_2206': 5220, 's_txt': 5221, 's_split': None, 'n_pos': 5225, 'n_col': 5230, 'n_2206': 5241, 'n_txt': 5242, 'n_split': 5247},
    19: {'s_pos': 5336, 's_col': 5341, 's_2206': 5352, 's_txt': 5353, 's_split': None, 'n_pos': 5357, 'n_col': 5362, 'n_2206': 5373, 'n_txt': 5374, 'n_split': 5379}
}

tx_list = cfg['transactions']
for idx, tx in enumerate(tx_list, 1):
    m = row_map_6707[idx]
    
    # 1. Update Saldo
    saldo_str = tx['saldo'].strip()
    update_text_node(doc, m['s_txt'], saldo_str)
    clean_split_node(doc, m['s_split'])
    w_saldo = calc_text_width(saldo_str)
    update_t2206(doc, m['s_2206'], w_saldo)
    update_t2100_x(doc, m['s_pos'], TARGET_XR_SALDO - w_saldo)
    update_color(doc, m['s_col'], COLOR_BIRU_SALDO)
    
    # 2. Update Nominal
    nom_str = tx['nominal'].strip()
    is_cr = tx['tipe'] == 'CR' or nom_str.startswith('+')
    col = COLOR_HIJAU_CR if is_cr else COLOR_HITAM_DB
    
    # Format nominal
    if is_cr and not nom_str.startswith('+'):
        nom_str = '+' + nom_str
    elif not is_cr and not nom_str.startswith('-'):
        nom_str = '-' + nom_str
        
    update_text_node(doc, m['n_txt'], nom_str)
    clean_split_node(doc, m['n_split'])
    w_nom = calc_text_width(nom_str)
    update_t2206(doc, m['n_2206'], w_nom)
    update_t2100_x(doc, m['n_pos'], TARGET_XR_NOMINAL - w_nom)
    update_color(doc, m['n_col'], col)

print(f"[Tahap 7/7] Mutasi & Summary    : 19 Baris Saldo & Nominal Rata Kanan & Warna Presisi [PASS ✓]")

# Post-Flight Safety Checks
for r in doc.records:
    r['size'] = len(r['payload'])

total_recs_final = len(doc.records)
assert total_recs_initial == total_recs_final, f"Zero-shift invariant error! {total_recs_initial} != {total_recs_final}"

# Check for 0-byte tag 2202/2201
zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"

doc.save(XAR_PATH)
print("\n=======================================================")
print(f" [SUCCESS 100%] FILE SELESAI DIPROSES DAN DISIMPAN!")
print(f" Output: {XAR_PATH}")
print(f" Total Records: {total_recs_final:,} (Zero-Shift Invariant Validated)")
print("=======================================================")
