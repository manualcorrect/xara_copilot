"""
MASTER PIPELINE EXECUTOR: execute_adhikarya_jun_pipeline.py
Automated 7-Stage Processor for Mandiri e-Statement
Customer: ADHIKARYA PUTRA
Period: JUN 2026 (13 Pages, 147 Transaction Rows)
SOP Project V2 Standard Compliant
"""

import os
import sys
import json
import struct
import openpyxl
from datetime import datetime, date, time
from xar_dom_engine import XarDocument

# Ensure unbuffered UTF-8 output
sys.stdout.reconfigure(encoding='utf-8', line_buffering=True, errors='replace')

# =========================================================================
# GLYPH ADVANCE WIDTHS FOR TTInterphases-Bold (H=6559 mp)
# =========================================================================
CHAR_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(CHAR_WIDTHS.get(c, 4800) for c in text)

TARGET_XR_NOMINAL = 431250 # 15.214 cm
TARGET_XR_SALDO   = 570250 # 20.049 cm

# Native Palette Dictionary for 0.xar (37,198 records)
COLOR_GREEN = bytearray.fromhex('ee030000') # Native Green (CR / Dana Masuk)
COLOR_BLACK = bytearray.fromhex('9e010000') # Native Black (DB / Dana Keluar)
COLOR_BLUE  = bytearray.fromhex('50050000') # Native Blue (Saldo Akhir / Running Saldo)
COLOR_GRAY  = bytearray.fromhex('8a030000') # Native Dark Gray (Saldo Awal)
COLOR_TEXT  = bytearray.fromhex('58040000') # Native Black Text

def fmt_idr(val):
    if isinstance(val, (int, float)):
        num = float(val)
    else:
        s = str(val).strip().replace('+', '').replace('-', '').replace(' ', '')
        if ',' in s and '.' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            s = s.replace(',', '.')
        num = float(s or 0.0)
    return f"{abs(num):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def update_text(doc, rec_idx, text_str):
    p = bytearray(text_str.encode('utf-16le'))
    doc.records[rec_idx]['payload'] = p
    doc.records[rec_idx]['size'] = len(p)

def blank_node(doc, rec_idx):
    if rec_idx is not None:
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

def update_color(doc, rec_idx, color_bytes):
    if rec_idx is not None:
        doc.records[rec_idx]['payload'] = color_bytes
        doc.records[rec_idx]['size'] = len(color_bytes)

def update_t2206(doc, rec_idx, new_w):
    if rec_idx is not None:
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_w, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_t2100_x(doc, rec_idx, new_x):
    if rec_idx is not None:
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def sync_and_save(doc, out_path, expected_recs=37198):
    for r in doc.records:
        r['size'] = len(r['payload'])
    assert len(doc.records) == expected_recs, f"Zero-shift violation! Expected {expected_recs}, got {len(doc.records)}"
    zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
    assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"
    doc.save(out_path)
    print(f"   [SAVED] {os.path.basename(out_path)} ({len(doc.records):,} records) [100% PASS]")

def run_adhikarya_jun_pipeline():
    folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUN'
    base_xar = os.path.join(folder, '0.xar')
    excel_path = os.path.join(folder, 'Template_Pekerjaan_Xara_Jun.xlsx')

    print("=========================================================================")
    print("   PROJECT V2 PIPELINE EXECUTION: ADHIKARYA PUTRA JUN 2026")
    print("   Target: 13 Pages, 147 Transaction Rows")
    print(f"   Base File: {base_xar}")
    print(f"   Excel File: {excel_path}")
    print("=========================================================================\n")

    # Load Excel data
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws_header = wb['Header & Ringkasan']
    ws_mutasi = wb['Tabel_Mutasi']

    # Extract header values using key search in Col A
    header_dict = {}
    for r in range(1, 30):
        k = ws_header.cell(r, 1).value
        v = ws_header.cell(r, 2).value
        if k:
            header_dict[str(k).strip()] = v

    nama_nasabah = str(header_dict.get('Nama Nasabah (Tahap 1)', 'Adhikarya Putra')).strip()
    if not nama_nasabah.endswith(" "):
        nama_nasabah += " "
    periode_laporan = str(header_dict.get('Periode Laporan (Tahap 2)', '01 Jun 2026 - 30 Jun 2026')).strip()
    dicetak_pada = str(header_dict.get('Dicetak Pada (Tahap 3)', '10 Sep 2026')).strip()
    nomor_rekening = str(header_dict.get('Nomor Rekening (Tahap 4)', '1630016148929')).strip()
    if not nomor_rekening.endswith(" "):
        nomor_rekening += " "

    saldo_awal = float(header_dict.get('Saldo Awal', 52488.81))
    dana_masuk = float(header_dict.get('Dana Masuk (Kredit)', 30212000))
    dana_keluar = float(header_dict.get('Dana Keluar (Debit)', 29693990))
    saldo_akhir = float(header_dict.get('Saldo Akhir', 570498.81))

    print(f"[*] Configuration Loaded:")
    print(f"    - Nama Nasabah   : '{nama_nasabah}'")
    print(f"    - Periode        : '{periode_laporan}'")
    print(f"    - Dicetak Pada   : '{dicetak_pada}'")
    print(f"    - Nomor Rekening : '{nomor_rekening}'")
    print(f"    - Saldo Awal     : {saldo_awal:,.2f}")
    print(f"    - Dana Masuk     : {dana_masuk:,.2f}")
    print(f"    - Dana Keluar    : {dana_keluar:,.2f}")
    print(f"    - Saldo Akhir    : {saldo_akhir:,.2f}")

    # Load transactions from Excel (rows 6 to 152)
    tx_list = []
    for r in range(6, 153):
        no_val = ws_mutasi.cell(r, 1).value
        date_val = ws_mutasi.cell(r, 2).value
        time_val = ws_mutasi.cell(r, 3).value
        desc_val = ws_mutasi.cell(r, 4).value
        nom_val = ws_mutasi.cell(r, 5).value
        type_val = ws_mutasi.cell(r, 6).value
        bal_val = ws_mutasi.cell(r, 7).value
        tx_list.append({
            'row_num': r - 5,
            'excel_row': r,
            'date_raw': date_val,
            'time_raw': time_val,
            'desc': desc_val,
            'nominal': nom_val,
            'type': 'CR' if nom_val > 0 else 'DB',
            'balance': bal_val
        })

    assert len(tx_list) == 147, f"Expected 147 transactions, got {len(tx_list)}"
    print(f"[*] Loaded {len(tx_list)} transactions from Excel.")

    # Load Rows Map
    with open('adhikarya_jun_rows_map.json', 'r', encoding='utf-8') as f:
        rows_map = json.load(f)
    assert len(rows_map) == 147, f"Expected 147 mapped rows, got {len(rows_map)}"

    # =========================================================================
    # [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH (13 HALAMAN)
    # =========================================================================
    print("\n--- [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH ---")
    doc1 = XarDocument(base_xar)
    TOTAL_RECS = len(doc1.records)

    name_recs = [1010, 3645, 6409, 9227, 12042, 14899, 17797, 20606, 23435, 26236, 29079, 31899, 34679]
    for p_idx, n_rec in enumerate(name_recs, 1):
        update_text(doc1, n_rec, nama_nasabah)
        # Update Tag 2206 width if present before name
        k_rec = n_rec - 1
        if doc1.records[k_rec]['tag'] == 2206:
            update_t2206(doc1, k_rec, calc_text_width(nama_nasabah))

    out_t1 = os.path.join(folder, '0_tahap1.xar')
    sync_and_save(doc1, out_t1, TOTAL_RECS)

    # =========================================================================
    # [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN (13 HALAMAN)
    # =========================================================================
    print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
    doc2 = XarDocument(out_t1)

    period_recs_map = [
        # (p_idx, rec_0, rec_1, rec_month_sep, rec_day2_tens, rec_day2_units)
        (1, 1043, 1047, 1055, 1056, 1061),
        (2, 3678, 3682, 3690, 3691, 3696),
        (3, 6442, 6446, 6454, 6455, 6460),
        (4, 9260, 9264, 9272, 9273, 9278),
        (5, 12075, 12079, 12087, 12088, 12093),
        (6, 14932, 14936, 14944, 14945, 14950),
        (7, 17830, 17834, 17842, 17843, 17848),
        (8, 20639, 20643, 20651, 20652, 20657),
        (9, 23468, 23472, 23480, 23481, 23486),
        (10, 26269, 26273, 26281, 26282, 26287),
        (11, 29112, 29116, 29124, 29125, 29130),
        (12, 31932, 31936, 31944, 31945, 31950),
        (13, 34712, 34716, 34724, 34725, 34730),
    ]

    for p_num, r0, r1, r_msep, r_d2t, r_d2u in period_recs_map:
        update_text(doc2, r0, "0")
        update_text(doc2, r1, "1")
        update_text(doc2, r_msep, "Jun 2026 - ")
        update_text(doc2, r_d2t, "3")
        update_text(doc2, r_d2u, "0 Jun 2026")

    out_t2 = os.path.join(folder, '0_tahap2.xar')
    sync_and_save(doc2, out_t2, TOTAL_RECS)

    # =========================================================================
    # [3/7] TAHAP 3: PERUBAHAN TANGGAL CETAK (13 HALAMAN)
    # =========================================================================
    print("\n--- [3/7] TAHAP 3: PERUBAHAN TANGGAL CETAK ---")
    doc3 = XarDocument(out_t2)

    # '10 Sep 2026' -> rec_d1='1', rec_d2='0', rec_my='Sep 2026'
    issued_recs_map = [
        (1, 1073, 1077, 1085),
        (2, 3708, 3712, 3720),
        (3, 6472, 6476, 6484),
        (4, 9290, 9294, 9302),
        (5, 12105, 12109, 12117),
        (6, 14962, 14966, 14974),
        (7, 17860, 17864, 17872),
        (8, 20669, 20673, 20681),
        (9, 23498, 23502, 23510),
        (10, 26299, 26303, 26311),
        (11, 29142, 29146, 29154),
        (12, 31962, 31966, 31974),
        (13, 34742, 34746, 34754),
    ]

    for p_num, rd1, rd2, rmy in issued_recs_map:
        update_text(doc3, rd1, "1")
        update_text(doc3, rd2, "0")
        update_text(doc3, rmy, "Sep 2026")

    out_t3 = os.path.join(folder, '0_tahap3.xar')
    sync_and_save(doc3, out_t3, TOTAL_RECS)

    # =========================================================================
    # [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING (HEADER HALAMAN 1)
    # =========================================================================
    print("\n--- [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING ---")
    doc4 = XarDocument(out_t3)

    acc_rec = 1108
    update_text(doc4, acc_rec, nomor_rekening)

    out_t4 = os.path.join(folder, '0_tahap4.xar')
    sync_and_save(doc4, out_t4, TOTAL_RECS)

    # =========================================================================
    # [5/7] TAHAP 5: PENOMORAN HALAMAN (13 HALAMAN)
    # =========================================================================
    print("\n--- [5/7] TAHAP 5: PENOMORAN HALAMAN ---")
    doc5 = XarDocument(out_t4)

    # All 13 pages are already cleanly structured as '1 of 13' .. '13 of 13' and '1 dari 13' .. '13 dari 13'
    out_t5 = os.path.join(folder, '0_tahap5.xar')
    sync_and_save(doc5, out_t5, TOTAL_RECS)

    # =========================================================================
    # [6/7] TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI (147 BARIS)
    # =========================================================================
    print("\n--- [6/7] TAHAP 6: TANGGAL & JAM TRANSAKSI (147 BARIS) ---")
    doc6 = XarDocument(out_t5)

    for r_num_str, m in rows_map.items():
        r_num = int(r_num_str)
        tx = tx_list[r_num - 1]
        
        # 1. Date update
        d_recs = m.get('d_recs', [])
        if d_recs:
            if len(d_recs) == 1:
                old_d = doc6.records[d_recs[0][0]]['payload'].decode('utf-16le', errors='ignore')
                new_d = old_d.replace('Apr 2026', 'Jun 2026').replace('Apr 202', 'Jun 202')
                if r_num == 131:
                    new_d = "25 Jun 2026"
                elif r_num == 147:
                    new_d = "30 Jun 2026"
                update_text(doc6, d_recs[0][0], new_d)
            elif len(d_recs) >= 2:
                # First node: e.g. '01 Apr 202' -> '01 Jun 202'
                old_d0 = doc6.records[d_recs[0][0]]['payload'].decode('utf-16le', errors='ignore')
                new_d0 = old_d0.replace('Apr 2026', 'Jun 2026').replace('Apr 202', 'Jun 202')
                if r_num == 131:
                    new_d0 = "25 Jun 202"
                elif r_num == 147:
                    new_d0 = "30 Jun 202"
                update_text(doc6, d_recs[0][0], new_d0)
                # Second node: '6'
                update_text(doc6, d_recs[1][0], "6")
                
        # 2. Time update
        t_recs = m.get('t_recs', [])
        if t_recs:
            if r_num == 131:
                update_text(doc6, t_recs[0][0], "04:00:00 WIB")
                for sec_r in t_recs[1:]:
                    blank_node(doc6, sec_r[0])
            elif r_num == 147:
                update_text(doc6, t_recs[0][0], "23:59:00 WIB")
                for sec_r in t_recs[1:]:
                    blank_node(doc6, sec_r[0])
            else:
                # Keep original time, if split keep primary + secondary
                pass

    out_t6 = os.path.join(folder, '0_tahap6.xar')
    sync_and_save(doc6, out_t6, TOTAL_RECS)

    # =========================================================================
    # [7/7] TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI (147 BARIS)
    # =========================================================================
    print("\n--- [7/7] TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI ---")
    doc7 = XarDocument(out_t6)

    # 1. Financial Summary Header
    # Saldo Awal: Rec 1209 ('52.488,81 ')
    str_sawal = f"{fmt_idr(saldo_awal)} "
    update_text(doc7, 1209, str_sawal)
    update_color(doc7, 1205, COLOR_GRAY)
    update_t2206(doc7, 1197, calc_text_width(str_sawal))

    # Dana Masuk: Rec 1219 ('+ 30.212.000,00'), Rec 1224 (blank)
    str_dmasuk = f"+ {fmt_idr(dana_masuk)}"
    update_text(doc7, 1219, str_dmasuk)
    blank_node(doc7, 1224)
    update_color(doc7, 1215, COLOR_GREEN)
    update_t2206(doc7, 1213, calc_text_width(str_dmasuk))

    # Dana Keluar: Rec 1238 ('- 29.693.990,00 ')
    str_dkeluar = f"- {fmt_idr(dana_keluar)} "
    update_text(doc7, 1238, str_dkeluar)
    update_color(doc7, 1231, COLOR_BLACK)
    update_t2206(doc7, 1229, calc_text_width(str_dkeluar))

    # Saldo Akhir: Rec 1252 ('570.498,81')
    str_sakhir = f"{fmt_idr(saldo_akhir)}"
    update_text(doc7, 1252, str_sakhir)
    update_color(doc7, 1245, COLOR_BLUE)
    update_t2206(doc7, 1242, calc_text_width(str_sakhir))

    print(f"   [*] Header Summary updated:")
    print(f"       - Saldo Awal  : '{str_sawal.strip()}' (Dark Gray)")
    print(f"       - Dana Masuk  : '{str_dmasuk}' (Green)")
    print(f"       - Dana Keluar : '{str_dkeluar.strip()}' (Black)")
    print(f"       - Saldo Akhir : '{str_sakhir}' (Blue)")

    # 2. Update all 147 Transaction Rows (Nominal, Saldo, Split Cleaning, Alignment)
    for r_num_str, m in rows_map.items():
        r_num = int(r_num_str)
        tx = tx_list[r_num - 1]

        # Saldo update
        s_rec = m['s_txt']
        s_splits = m.get('s_splits', [])
        s_2206 = m.get('s_2206')
        s_2100 = m.get('s_2100')

        bal_val = tx['balance']
        str_saldo = fmt_idr(bal_val)
        update_text(doc7, s_rec, str_saldo)
        for sp in s_splits:
            blank_node(doc7, sp)

        # Saldo width update
        w_saldo = calc_text_width(str_saldo)
        if s_2206:
            update_t2206(doc7, s_2206, w_saldo)

        # Nominal update
        n_rec = m['n_txt']
        n_splits = m.get('n_splits', [])
        n_150 = m.get('n_150')
        n_2206 = m.get('n_2206')
        n_2100 = m.get('n_2100')

        nom_val = tx['nominal']
        if nom_val > 0:
            str_nominal = f"+{fmt_idr(nom_val)}"
            nom_color = COLOR_GREEN
        else:
            str_nominal = f"-{fmt_idr(abs(nom_val))}"
            nom_color = COLOR_BLACK

        update_text(doc7, n_rec, str_nominal)
        for sp in n_splits:
            blank_node(doc7, sp)

        if n_150:
            update_color(doc7, n_150, nom_color)

        w_nominal = calc_text_width(str_nominal)
        new_x_left = TARGET_XR_NOMINAL - w_nominal
        if n_2100:
            update_t2100_x(doc7, n_2100, new_x_left)
        if n_2206:
            update_t2206(doc7, n_2206, w_nominal)

    out_t7 = os.path.join(folder, '0_tahap7.xar')
    sync_and_save(doc7, out_t7, TOTAL_RECS)

    print("\n=========================================================================")
    print("   [SUCCESS] PIPELINE 7 TAHAP ADHIKARYA PUTRA JUN 2026 SELESAI 100%!")
    print(f"   Final Master Output: {out_t7}")
    print("=========================================================================\n")

if __name__ == '__main__':
    run_adhikarya_jun_pipeline()
