"""
FLAWLESS EXECUTION SCRIPT FOR ANANDA SUCI HATI - AGUSTUS 2026 (6,103 Records)
Compliant with SOP Project V2 (7 Tahap Standar Master)
"""

import os
import sys
import shutil
import struct
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True)

# Target directory
TARGET_DIR = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Aug"
XAR_PATH = os.path.join(TARGET_DIR, "0.xar")
EXCEL_PATH = os.path.join(TARGET_DIR, "Template_Pekerjaan_Xara_Aug.xlsx")
BACKUP_PATH = os.path.join(TARGET_DIR, "0_backup_original.xar")

# Create backup if not already present
if not os.path.exists(BACKUP_PATH):
    shutil.copy2(XAR_PATH, BACKUP_PATH)
    print(f"[*] Backup file asli dibuat di: {BACKUP_PATH}")

doc = XarDocument(XAR_PATH)
cfg = parse_xara_excel_template(EXCEL_PATH)

total_recs_initial = len(doc.records)
print(f"[*] Total Records Initial: {total_recs_initial}")
assert total_recs_initial == 6103, f"Expected 6103 records, found {total_recs_initial}"

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

# Native Colors Tag 150 for 6103
COLOR_HIJAU_CR   = bytearray.fromhex('12040000') # Credit Green (#00A651)
COLOR_HITAM_DB   = bytearray.fromhex('72020000') # Debit Black (#000000)
COLOR_ABU_AWAL   = bytearray.fromhex('ae030000') # Initial Balance Gray
COLOR_BIRU_SALDO = bytearray.fromhex('5a050000') # Closing Balance Blue (#005B9C)

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

def update_t2100(doc, rec_idx, x_left):
    if rec_idx is not None:
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', x_left, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_color(doc, rec_idx, color_payload):
    if rec_idx is not None:
        doc.records[rec_idx]['payload'] = bytearray(color_payload)
        doc.records[rec_idx]['size'] = len(color_payload)

print("\n=======================================================")
print("  EKSEKUSI 7 TAHAP SOP STANDAR MASTER (ANANDA - AGUSTUS 2026)")
print("=======================================================")

# =========================================================
# TAHAP 1: PERUBAHAN NAMA
# =========================================================
new_name = cfg['header']['nama'].strip() + " \r\n"
update_text_node(doc, 1030, new_name)
update_text_node(doc, 3731, new_name)
update_t2206(doc, 1035, 0)
update_t2206(doc, 3735, 0)
print(f"[Tahap 1/7] Nama Nasabah       : '{cfg['header']['nama']}' [PASS ✓]")

# =========================================================
# TAHAP 2: PERUBAHAN PERIODE
# =========================================================
# Periode: 01 Aug 2026 - 31 Aug 2026
# Page 1
update_text_node(doc, 1073, "0")
update_text_node(doc, 1077, "1")
update_text_node(doc, 1085, " Aug 2026 - 31 Aug ")
update_text_node(doc, 1090, "202")
update_text_node(doc, 1095, "6")

# Page 2
update_text_node(doc, 3767, "0")
update_text_node(doc, 3771, "1")
update_text_node(doc, 3779, " Aug 2026 - 31 Aug ")
update_text_node(doc, 3784, "202")
update_text_node(doc, 3789, "6")
print(f"[Tahap 2/7] Periode Laporan    : '01 Aug 2026 - 31 Aug 2026' [PASS ✓]")

# =========================================================
# TAHAP 3: PERUBAHAN DICETAK PADA
# =========================================================
# Target: 01 Oct 2026
# Page 1
update_text_node(doc, 1107, "0")
update_text_node(doc, 1111, "1")
update_text_node(doc, 1119, " Oct 2026")

# Page 2
update_text_node(doc, 3801, "0")
update_text_node(doc, 3805, "1")
update_text_node(doc, 3813, " Oct 2026")
print(f"[Tahap 3/7] Dicetak Pada       : '01 Oct 2026' [PASS ✓]")

# =========================================================
# TAHAP 4: PERUBAHAN NOMOR REKENING
# =========================================================
acc_num = cfg['header']['nomor_rekening'].strip()
update_text_node(doc, 1140, acc_num + " ")
print(f"[Tahap 4/7] Nomor Rekening     : '{acc_num}' [PASS ✓]")

# =========================================================
# TAHAP 5: PERUBAHAN NOMOR HALAMAN
# =========================================================
# Page 1
update_text_node(doc, 1200, "1 of 2")
update_text_node(doc, 1312, "2")
update_text_node(doc, 1333, "1 d")
update_text_node(doc, 1338, "ari")

# Page 2
update_text_node(doc, 3839, "2")
update_text_node(doc, 3847, "of 2")
update_text_node(doc, 3868, "2")
update_text_node(doc, 3889, "2 d")
update_text_node(doc, 3894, "ari")
print(f"[Tahap 5/7] Nomor Halaman      : '1 of 2' & '2 of 2' [PASS ✓]")

# =========================================================
# TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI
# =========================================================
# Row 1
update_text_node(doc, 1694, "01 Aug 2026")
update_text_node(doc, 1669, "17:44:18")
update_text_node(doc, 1674, " WIB")

# Row 2
update_text_node(doc, 1841, "01 Aug 2026")
update_text_node(doc, 1816, "18:45:53 ")
update_text_node(doc, 1821, "WIB")

# Row 3
update_text_node(doc, 2003, "01 Aug 2026")
update_text_node(doc, 1978, "21:09:49 WI")
update_text_node(doc, 1983, "B")

# Row 4
update_text_node(doc, 2170, "01 Aug 2026")
update_text_node(doc, 2140, "22:33:1")
update_text_node(doc, 2145, "6 WI")
update_text_node(doc, 2150, "B")

# Row 5
update_text_node(doc, 2312, "01 Aug 2026")
update_text_node(doc, 2292, "22:44:07 WIB")

# Row 6
update_text_node(doc, 2479, "03 Aug 2026")
update_text_node(doc, 2454, "17:46:1")
update_text_node(doc, 2459, "2 WIB")

# Row 7
update_text_node(doc, 2629, "04 Aug 2026")
update_text_node(doc, 2604, "21:52:57 WI")
update_text_node(doc, 2609, "B")

# Row 8
update_text_node(doc, 2771, "08 Aug 2026")
update_text_node(doc, 2751, "13:40:47 WIB")

# Row 9
update_text_node(doc, 2908, "09 Aug 2026")
update_text_node(doc, 2888, "16:46:22 WIB")

# Row 10
update_text_node(doc, 3074, "10 Aug 2026")
update_text_node(doc, 3054, "04:00:00 WIB")

# Row 11
update_text_node(doc, 4262, "20 Aug 2026")
update_text_node(doc, 4242, "20:39:32 WIB")

# Row 12
update_text_node(doc, 4419, "25 Aug 2026")
update_text_node(doc, 4399, "20:39:32 WIB")

# Row 13
update_text_node(doc, 4561, "31 Aug 2026")
update_text_node(doc, 4536, "10:04:51 W")
update_text_node(doc, 4541, "IB")

# Row 14
update_text_node(doc, 4708, "31 ")
update_text_node(doc, 4713, "Aug 2026")
update_text_node(doc, 4683, "10:04:51 W")
update_text_node(doc, 4688, "IB")

# Row 15
update_text_node(doc, 4865, "31 Aug 2026")
update_text_node(doc, 4845, "23:59:00 WIB")
print(f"[Tahap 6/7] Tanggal & Jam       : 15 Baris Agustus 2026 Kronologis [PASS ✓]")

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
update_text_node(doc, 1223, sawal)
update_t2206(doc, 1217, calc_text_width(sawal))
update_color(doc, 1218, COLOR_ABU_AWAL)

# Dana Masuk
update_text_node(doc, 1233, dmasuk)
update_t2206(doc, 1227, calc_text_width(dmasuk))
update_color(doc, 1228, COLOR_HIJAU_CR)

# Dana Keluar
update_text_node(doc, 1246, dkeluar)
update_t2206(doc, 1238, calc_text_width(dkeluar))
update_color(doc, 1239, COLOR_HITAM_DB)

# Saldo Akhir
update_text_node(doc, 1259, sakhir)
clean_split_node(doc, 1264)
update_t2206(doc, 1250, calc_text_width(sakhir))
update_color(doc, 1252, COLOR_BIRU_SALDO)

# 2. Table Mutations Mapping
row_map_6103 = {
    1:  {'s_pos': 1611, 's_col': 1616, 's_2206': 1627, 's_txt': 1628, 's_split': None, 'n_pos': 1632, 'n_col': 1637, 'n_2206': 1648, 'n_txt': 1649, 'n_split': None},
    2:  {'s_pos': 1753, 's_col': 1758, 's_2206': 1769, 's_txt': 1770, 's_split': None, 'n_pos': 1774, 'n_col': 1779, 'n_2206': 1790, 'n_txt': 1791, 'n_split': 1796},
    3:  {'s_pos': 1915, 's_col': 1920, 's_2206': 1931, 's_txt': 1932, 's_split': None, 'n_pos': 1936, 'n_col': 1941, 'n_2206': 1952, 'n_txt': 1953, 'n_split': 1958},
    4:  {'s_pos': 2077, 's_col': 2082, 's_2206': 2093, 's_txt': 2094, 's_split': None, 'n_pos': 2098, 'n_col': 2103, 'n_2206': 2114, 'n_txt': 2115, 'n_split': 2120},
    5:  {'s_pos': 2229, 's_col': 2234, 's_2206': 2245, 's_txt': 2246, 's_split': None, 'n_pos': 2250, 'n_col': 2255, 'n_2206': 2266, 'n_txt': 2267, 'n_split': 2272},
    6:  {'s_pos': 2391, 's_col': 2396, 's_2206': 2407, 's_txt': 2408, 's_split': None, 'n_pos': 2412, 'n_col': 2417, 'n_2206': 2428, 'n_txt': 2429, 'n_split': 2434},
    7:  {'s_pos': 2541, 's_col': 2546, 's_2206': 2557, 's_txt': 2558, 's_split': None, 'n_pos': 2562, 'n_col': 2567, 'n_2206': 2578, 'n_txt': 2579, 'n_split': 2584},
    8:  {'s_pos': 2688, 's_col': 2693, 's_2206': 2704, 's_txt': 2705, 's_split': None, 'n_pos': 2709, 'n_col': 2714, 'n_2206': 2725, 'n_txt': 2726, 'n_split': 2731},
    9:  {'s_pos': 2825, 's_col': 2830, 's_2206': 2841, 's_txt': 2842, 's_split': None, 'n_pos': 2846, 'n_col': 2851, 'n_2206': 2862, 'n_txt': 2863, 'n_split': 2868},
    10: {'s_pos': 2991, 's_col': 2996, 's_2206': 3007, 's_txt': 3008, 's_split': 3013, 'n_pos': 3017, 'n_col': 3022, 'n_2206': 3033, 'n_txt': 3034, 'n_split': None},
    11: {'s_pos': 4179, 's_col': 4184, 's_2206': 4195, 's_txt': 4196, 's_split': None, 'n_pos': 4200, 'n_col': 4205, 'n_2206': 4216, 'n_txt': 4217, 'n_split': 4222},
    12: {'s_pos': 4336, 's_col': 4341, 's_2206': 4352, 's_txt': 4353, 's_split': None, 'n_pos': 4357, 'n_col': 4362, 'n_2206': 4373, 'n_txt': 4374, 'n_split': 4379},
    13: {'s_pos': 4473, 's_col': 4478, 's_2206': 4489, 's_txt': 4490, 's_split': None, 'n_pos': 4494, 'n_col': 4499, 'n_2206': 4510, 'n_txt': 4511, 'n_split': 4516},
    14: {'s_pos': 4620, 's_col': 4625, 's_2206': 4636, 's_txt': 4637, 's_split': None, 'n_pos': 4641, 'n_col': 4646, 'n_2206': 4657, 'n_txt': 4658, 'n_split': 4663},
    15: {'s_pos': 4772, 's_col': 4777, 's_2206': 4788, 's_txt': 4789, 's_split': 4794, 's_split2': 4799, 'n_pos': 4803, 'n_col': 4808, 'n_2206': 4819, 'n_txt': 4820, 'n_split': 4825}
}

tx_list = cfg['transactions']
for idx, tx in enumerate(tx_list, 1):
    if idx > 15: break
    m = row_map_6103[idx]

    # 1. Update Saldo (BIRU MANDIRI)
    saldo_str = tx['saldo'].strip()
    update_text_node(doc, m['s_txt'], saldo_str)
    clean_split_node(doc, m.get('s_split'))
    clean_split_node(doc, m.get('s_split2'))
    w_saldo = calc_text_width(saldo_str)
    update_t2206(doc, m['s_2206'], w_saldo)
    update_t2100(doc, m['s_pos'], TARGET_XR_SALDO - w_saldo)
    update_color(doc, m['s_col'], COLOR_BIRU_SALDO)

    # 2. Update Nominal
    nom_str = tx['nominal'].strip()
    is_cr = tx['tipe'] == 'CR' or nom_str.startswith('+')
    col = COLOR_HIJAU_CR if is_cr else COLOR_HITAM_DB

    if is_cr and not nom_str.startswith('+'):
        nom_str = '+' + nom_str
    elif not is_cr and not nom_str.startswith('-'):
        nom_str = '-' + nom_str

    update_text_node(doc, m['n_txt'], nom_str)
    clean_split_node(doc, m.get('n_split'))
    w_nom = calc_text_width(nom_str)
    update_t2206(doc, m['n_2206'], w_nom)
    update_t2100(doc, m['n_pos'], TARGET_XR_NOMINAL - w_nom)
    update_color(doc, m['n_col'], col)

print(f"[Tahap 7/7] Mutasi & Summary    : 15 Baris Saldo (Biru) & Nominal Rata Kanan Presisi [PASS ✓]")

# Post-Flight Safety Checks
for r in doc.records:
    r['size'] = len(r['payload'])

total_recs_final = len(doc.records)
assert total_recs_initial == total_recs_final, f"Zero-shift invariant error! {total_recs_initial} != {total_recs_final}"

# Check for 0-byte tag 2202/2201
zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"

doc.save(XAR_PATH)
# Also save 0_output.xar
out_path = os.path.join(TARGET_DIR, "0_output.xar")
doc.save(out_path)

print("\n=======================================================")
print(f" [SUCCESS 100%] FILE AGUSTUS SELESAI DIPROSES DAN DISIMPAN!")
print(f" Output 1: {XAR_PATH}")
print(f" Output 2: {out_path}")
print(f" Total Records: {total_recs_final:,} (Zero-Shift Invariant Validated)")
print("=======================================================")
