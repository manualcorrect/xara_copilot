"""
MASTER FLAWLESS EXECUTOR: execute_flawless_jul_10536.py
Processes Mandiri 3-Page 10,536-record e-Statement (Jul 2026)
Compliant with SOP Project V2 (Tahap 1 - 7 + Tahap 8 Precision Alignment)
"""

import os
import sys
import json
import struct
import shutil
from datetime import datetime
from xar_dom_engine import XarDocument

# Target paths
target_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul"
in_xar = os.path.join(target_dir, "0.xar")
out_xar = os.path.join(target_dir, "0_output.xar")

print("=========================================================================")
print("   PROJECT V2 PIPELINE EXECUTION: JULI 2026 (3 PAGES / 34 TRANSACTIONS)")
print(f"   Source XAR : {in_xar}")
print(f"   Output XAR : {out_xar}")
print("=========================================================================\n")

# Load mapping and schedule
with open("perfect_34_rows_map.json", "r", encoding="utf-8") as f:
    rows_map = json.load(f)

with open("jul_34_schedule.json", "r", encoding="utf-8") as f:
    schedule = json.load(f)

# Native Colors for 10,536-record 0.xar
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

# Helper mutation functions
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
NAME_STR = "MASRIYAH MUHAMMAD "
for name_idx in [3083, 5945, 8964]:
    update_text(doc, name_idx, NAME_STR)
print(f"  [OK] Nama Nasabah diubah ke '{NAME_STR}' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 2: PERUBAHAN PERIODE LAPORAN (3 HALAMAN)
# =========================================================================
print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
# Periode: 01 Jul 2026 - 31 Jul 2026
# Page 1: 961='0', 965='1', 973='Jul 2026 - 31 Jul 202', 978='6'
update_text(doc, 961, "0")
update_text(doc, 965, "1 ")
update_text(doc, 973, "Jul 2026 - 31 Jul 202")
update_text(doc, 978, "6")

# Page 2: 3622='0', 3626='1', 3634='Jul 2026 - 31 Jul 202', 3639='6'
update_text(doc, 3622, "0")
update_text(doc, 3626, "1 ")
update_text(doc, 3634, "Jul 2026 - 31 Jul 202")
update_text(doc, 3639, "6")

# Page 3: 6484='0', 6488='1', 6496='Jul 2026 - 31 Jul 202', 6501='6'
update_text(doc, 6484, "0")
update_text(doc, 6488, "1 ")
update_text(doc, 6496, "Jul 2026 - 31 Jul 202")
update_text(doc, 6501, "6")
print("  [OK] Periode Laporan diubah ke '01 Jul 2026 - 31 Jul 2026' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 3: PERUBAHAN DICETAK PADA (3 HALAMAN)
# =========================================================================
print("\n--- [3/7] TAHAP 3: PERUBAHAN DICETAK PADA ---")
# Dicetak pada: 01 Oct 2026
# Page 1: 989='0', 993='1', 1001='Oct 2026'
update_text(doc, 989, "0")
update_text(doc, 993, "1 ")
update_text(doc, 1001, "Oct 2026")

# Page 2: 3650='0', 3654='1', 3662='Oct 2026'
update_text(doc, 3650, "0")
update_text(doc, 3654, "1 ")
update_text(doc, 3662, "Oct 2026")

# Page 3: 6512='0', 6516='1', 6524='Oct 2026'
update_text(doc, 6512, "0")
update_text(doc, 6516, "1 ")
update_text(doc, 6524, "Oct 2026")
print("  [OK] Tanggal Dicetak Pada diubah ke '01 Oct 2026' pada Halaman 1, 2, 3.")

# =========================================================================
# TAHAP 4: PERUBAHAN NOMOR REKENING
# =========================================================================
print("\n--- [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING ---")
# Nomor Rekening: 1630016144514
update_text(doc, 1031, "1630016144514 ")
print("  [OK] Nomor Rekening diubah ke '1630016144514 ' pada Header Lembar 1.")

# =========================================================================
# TAHAP 5: PERUBAHAN NOMOR HALAMAN (SINKRONISASI HEADER & FOOTER)
# =========================================================================
print("\n--- [5/7] TAHAP 5: PERUBAHAN NOMOR HALAMAN (3 HALAMAN) ---")
# Page 1 Header & Footer
update_text(doc, 1210, "1 dari 3")
update_text(doc, 1079, "of 3")

# Page 2 Header & Footer
update_text(doc, 3728, "dari 3")
update_text(doc, 3695, "of 3")

# Page 3 Header & Footer
update_text(doc, 6590, "dari 3")
update_text(doc, 6557, "of 3")
print("  [OK] Penomoran Halaman diubah ke 'X dari 3' (Header) dan 'X of 3' (Footer).")

# =========================================================================
# TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI (34 BARIS)
# =========================================================================
print("\n--- [6/7] TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI ---")
for s in schedule:
    r_no = s['row_no']
    r_map = rows_map[r_no - 1]
    
    # 1. Update Time
    t_str = s['time']
    update_text(doc, r_map['time_primary'], t_str)
    for sp_idx in r_map['time_splits']:
        blank_split(doc, sp_idx)
        
    # 2. Update Date
    d_str = s['date'] # e.g. "01 Jul 2026"
    d_parts = d_str.split(" ")
    day_month = f"{d_parts[0]} {d_parts[1]} 20"
    year_digit = d_parts[2][2:] # e.g. "26"
    
    # If date is split into [DD MMM 20] + [26]
    if len(r_map['date_splits']) > 0:
        update_text(doc, r_map['date_primary'], day_month)
        update_text(doc, r_map['date_splits'][0], year_digit)
        for sp_idx in r_map['date_splits'][1:]:
            blank_split(doc, sp_idx)
    else:
        update_text(doc, r_map['date_primary'], d_str)

print(f"  [OK] Seluruh {len(schedule)} baris tanggal & jam berhasil di-update secara kronologis.")

# =========================================================================
# TAHAP 7: PERUBAHAN RINGKASAN HEADER, TABEL MUTASI, DAN ALIGNMENT RATA KANAN
# =========================================================================
print("\n--- [7/7] TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI UTAMA ---")

# 1. Summary Header
# Saldo Awal: 654.955,00
update_text(doc, 1101, "654.")
update_text(doc, 1106, "955,00 ")
update_color(doc, 1097, COLOR_AWAL_ABU)

# Dana Masuk: 8.347.206,00
update_text(doc, 1115, "+ ")
update_text(doc, 1120, "8.347.206,")
update_text(doc, 1125, "00")
update_color(doc, 1111, COLOR_CR_HIJAU)

# Dana Keluar: 8.731.651,00
update_text(doc, 1137, "- 8.731.")
update_text(doc, 1142, "651,00 ")
update_color(doc, 1131, COLOR_DB_HITAM)

# Saldo Akhir: 270.510,00
update_text(doc, 1154, "270.510,")
update_text(doc, 1159, "00")
update_color(doc, 1148, COLOR_SALDO_BIRU)
print("  [OK] Ringkasan Keuangan Header (Awal, Masuk, Keluar, Akhir) ter-update sempurna.")

# 2. 34 Transaction Rows: Nominal & Saldo
# Transactions from Template Excel:
transactions_data = [
    # Page 1 (Rows 1..10)
    {"no": 1, "nom": "-500.000,00", "saldo": "154.955,00", "is_cr": False},
    {"no": 2, "nom": "-14.000,00", "saldo": "140.955,00", "is_cr": False},
    {"no": 3, "nom": "+510.000,00", "saldo": "650.955,00", "is_cr": True},
    {"no": 4, "nom": "-500.000,00", "saldo": "150.955,00", "is_cr": False},
    {"no": 5, "nom": "-30.000,00", "saldo": "120.955,00", "is_cr": False},
    {"no": 6, "nom": "-90.000,00", "saldo": "30.955,00", "is_cr": False},
    {"no": 7, "nom": "+731.000,00", "saldo": "761.955,00", "is_cr": True},
    {"no": 8, "nom": "-30.000,00", "saldo": "731.955,00", "is_cr": False},
    {"no": 9, "nom": "+500.000,00", "saldo": "1.231.955,00", "is_cr": True},
    {"no": 10, "nom": "-600.000,00", "saldo": "631.955,00", "is_cr": False},

    # Page 2 (Rows 11..22)
    {"no": 11, "nom": "-100.000,00", "saldo": "531.955,00", "is_cr": False},
    {"no": 12, "nom": "-501.500,00", "saldo": "30.455,00", "is_cr": False},
    {"no": 13, "nom": "+519.000,00", "saldo": "549.455,00", "is_cr": True},
    {"no": 14, "nom": "-400.000,00", "saldo": "149.455,00", "is_cr": False},
    {"no": 15, "nom": "+500.000,00", "saldo": "649.455,00", "is_cr": True},
    {"no": 16, "nom": "-378.107,00", "saldo": "271.348,00", "is_cr": False},
    {"no": 17, "nom": "-119.000,00", "saldo": "152.348,00", "is_cr": False},
    {"no": 18, "nom": "+642.000,00", "saldo": "794.348,00", "is_cr": True},
    {"no": 19, "nom": "-92.000,00", "saldo": "702.348,00", "is_cr": False},
    {"no": 20, "nom": "-300.000,00", "saldo": "402.348,00", "is_cr": False},
    {"no": 21, "nom": "-40.000,00", "saldo": "362.348,00", "is_cr": False},
    {"no": 22, "nom": "-30.000,00", "saldo": "332.348,00", "is_cr": False},

    # Page 3 (Rows 23..34)
    {"no": 23, "nom": "+70.000,00", "saldo": "402.348,00", "is_cr": True},
    {"no": 24, "nom": "-152.999,00", "saldo": "249.349,00", "is_cr": False},
    {"no": 25, "nom": "-220.000,00", "saldo": "29.349,00", "is_cr": False},
    {"no": 26, "nom": "+4.860.206,00", "saldo": "4.889.555,00", "is_cr": True},
    {"no": 27, "nom": "-1.500.000,00", "saldo": "3.389.555,00", "is_cr": False},
    {"no": 28, "nom": "-100.757,00", "saldo": "3.288.798,00", "is_cr": False},
    {"no": 29, "nom": "-600.000,00", "saldo": "2.688.798,00", "is_cr": False},
    {"no": 30, "nom": "-2.500,00", "saldo": "2.686.298,00", "is_cr": False},
    {"no": 31, "nom": "-2.000.000,00", "saldo": "686.298,00", "is_cr": False},
    {"no": 32, "nom": "+15.000,00", "saldo": "701.298,00", "is_cr": True},
    {"no": 33, "nom": "-425.788,00", "saldo": "275.510,00", "is_cr": False},
    {"no": 34, "nom": "-5.000,00", "saldo": "270.510,00", "is_cr": False},
]

for tx in transactions_data:
    r_no = tx['no']
    r_map = rows_map[r_no - 1]
    
    # --- NOMINAL ---
    nom_str = tx['nom']
    is_cr = tx['is_cr']
    update_text(doc, r_map['nom_primary'], nom_str)
    for sp_idx in r_map['nom_splits']:
        blank_split(doc, sp_idx)
    
    # Tag 150 Color
    update_color(doc, r_map['nom_tag150'], COLOR_CR_HIJAU if is_cr else COLOR_DB_HITAM)
    
    # Ruler Right-Alignment (Tag 2100 & Tag 2206)
    nom_w = calc_text_width(nom_str)
    nom_x_left = TARGET_XR_NOMINAL - nom_w
    update_t2100(doc, r_map['nom_tag2100'], nom_x_left)
    update_t2206(doc, r_map['nom_tag2206'], nom_w)
    
    # --- SALDO ---
    saldo_str = tx['saldo']
    update_text(doc, r_map['saldo_primary'], saldo_str)
    for sp_idx in r_map['saldo_splits']:
        blank_split(doc, sp_idx)
        
    # Tag 150 Color
    update_color(doc, r_map['saldo_tag150'], COLOR_SALDO_BIRU)
    
    # Ruler Right-Alignment (Tag 2100 & Tag 2206)
    saldo_w = calc_text_width(saldo_str)
    saldo_x_left = TARGET_XR_SALDO - saldo_w
    update_t2100(doc, r_map['saldo_tag2100'], saldo_x_left)
    update_t2206(doc, r_map['saldo_tag2206'], saldo_w)

print(f"  [OK] Seluruh {len(transactions_data)} baris Nominal, Saldo, Warna, dan Alignment Rata Kanan berhasil di-update.")

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

# Also replace 0.xar with 0_output.xar for seamless live viewing / workflow
backup_0xar = os.path.join(target_dir, "0_ORIGINAL_BACKUP.xar")
if not os.path.exists(backup_0xar):
    shutil.copy2(in_xar, backup_0xar)
    print(f"[BACKUP] File asli di-backup ke: {backup_0xar}")

shutil.copy2(out_xar, in_xar)
print(f"[UPDATED] File 0.xar aktif telah diperbarui secara live.")
print("=========================================================================\n")
