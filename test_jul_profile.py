import os
import sys
import struct
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

# Colors
COLOR_HIJAU_CR   = bytearray.fromhex('ba030000') # #00A651
COLOR_HITAM_DB   = bytearray.fromhex('87010000') # #000000
COLOR_BIRU_SALDO = bytearray.fromhex('0d050000') # #005B9C
COLOR_ABU_AWAL   = bytearray.fromhex('96030000') # Dark Gray

GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

TARGET_XR_NOMINAL_7395 = 431250
TARGET_XR_SALDO_7395   = 570250

def update_text_node(doc, rec_idx, text_str):
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
        doc.records[rec_idx]['payload'] = color_payload
        doc.records[rec_idx]['size'] = len(color_payload)

def execute_mandiri_3page_7395(doc, cfg, quiet=False):
    """Execution profile for 3-Page Mandiri 7,395 records (Jul 2026)"""
    # 1. Tahap 1: Nama Nasabah
    new_name = cfg['header']['nama'].strip() + " "
    update_text_node(doc, 937, new_name)
    for c_idx in [942, 947, 952, 953, 958]:
        clean_split_node(doc, c_idx)
    update_text_node(doc, 3755, new_name)
    if not quiet: print(f"  [OK] Tahap 1 (Nama Nasabah) : '{new_name.strip()}' on Page 1 & Page 2")

    # 2. Tahap 2: Periode Laporan
    # Page 1:
    update_text_node(doc, 995, "0")
    update_text_node(doc, 999, "1")
    update_text_node(doc, 1007, " Jul 2026 - 31 Jul ")
    update_text_node(doc, 1012, "2026")
    # Page 2:
    update_text_node(doc, 3797, "0")
    update_text_node(doc, 3806, "1")
    update_text_node(doc, 3814, " Jul ")
    update_text_node(doc, 3815, "202")
    update_text_node(doc, 3820, "6 ")
    update_text_node(doc, 3825, "- ")
    update_text_node(doc, 3830, "3")
    update_text_node(doc, 3835, "1 ")
    update_text_node(doc, 3840, "Jul ")
    update_text_node(doc, 3841, "202")
    update_text_node(doc, 3846, "6")
    if not quiet: print(f"  [OK] Tahap 2 (Periode)      : '01 Jul 2026 - 31 Jul 2026' on Page 1 & Page 2")

    # 3. Tahap 3: Tanggal Cetak
    # Page 1:
    update_text_node(doc, 1023, "1")
    update_text_node(doc, 1027, "0")
    update_text_node(doc, 1035, " Sep 2026")
    # Page 2:
    update_text_node(doc, 3857, "1")
    update_text_node(doc, 3861, "0")
    update_text_node(doc, 3869, " Sep 2026")
    if not quiet: print(f"  [OK] Tahap 3 (Tanggal Cetak): '10 Sep 2026' on Page 1 & Page 2")

    # 4. Tahap 4: Nomor Rekening
    acc_str = cfg['header']['nomor_rekening'].strip() + " "
    update_text_node(doc, 1065, acc_str)
    clean_split_node(doc, 1074)
    if not quiet: print(f"  [OK] Tahap 4 (Nomor Rekening): '{acc_str.strip()}' on Header Page 1")

    # 5. Tahap 5: Nomor Halaman (Normalisasi 1..3)
    # Page 1:
    update_text_node(doc, 1117, "1 ")
    update_text_node(doc, 1122, "of 3")
    update_text_node(doc, 1232, "1 dari 3")
    # Page 2:
    update_text_node(doc, 3894, "2")
    update_text_node(doc, 3902, "of 3")
    update_text_node(doc, 3927, "2")
    update_text_node(doc, 3935, "dari 3")
    if not quiet: print(f"  [OK] Tahap 5 (Nomor Halaman): Normalized '1 of 3' & '2 of 3'")

    # 6. Tahap 6 & 7: Summary & Tabel Mutasi
    sawal = cfg['summary']['saldo_awal']
    dmasuk = cfg['summary']['dana_masuk']
    dkeluar = cfg['summary']['dana_keluar']
    sakhir = cfg['summary']['saldo_akhir']

    # Format numbers standard
    def fmt_idr(val_str, is_prefix=False):
        num = float(str(val_str).replace("+", "").replace("-", "").replace(".", "").replace(",", ".").replace(" ", "").strip() or 0.0)
        formatted = f"{num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        return formatted

    sawal_str = fmt_idr(sawal)
    dmasuk_str = "+ " + fmt_idr(dmasuk)
    dkeluar_str = "- " + fmt_idr(dkeluar)
    sakhir_str = fmt_idr(sakhir)

    # Summary: Saldo Awal (Rec 1142)
    update_text_node(doc, 1142, sawal_str)
    w_sawal = calc_text_width(sawal_str)
    update_t2206(doc, 1141, w_sawal)
    update_t2100(doc, 1146, TARGET_XR_SALDO_7395 - w_sawal)
    update_color(doc, 1131, COLOR_ABU_AWAL)

    # Summary: Dana Masuk (Rec 1468, 1473)
    update_text_node(doc, 1468, dmasuk_str)
    clean_split_node(doc, 1473)
    w_dmasuk = calc_text_width(dmasuk_str)
    update_t2206(doc, 1467, w_dmasuk)
    update_t2100(doc, 1477, TARGET_XR_NOMINAL_7395 - w_dmasuk)
    update_color(doc, 1457, COLOR_HIJAU_CR)

    # Summary: Dana Keluar (Rec 1163, 1164, 1169)
    update_text_node(doc, 1163, dkeluar_str)
    clean_split_node(doc, 1164)
    clean_split_node(doc, 1169)
    w_dkeluar = calc_text_width(dkeluar_str)
    update_t2206(doc, 1161, w_dkeluar)
    update_color(doc, 1162, COLOR_HITAM_DB)

    # Summary: Saldo Akhir (Rec 1176, 1181)
    update_text_node(doc, 1176, sakhir_str)
    clean_split_node(doc, 1181)
    w_sakhir = calc_text_width(sakhir_str)
    update_t2206(doc, 1173, w_sakhir)
    update_t2100(doc, 1185, TARGET_XR_SALDO_7395 - w_sakhir)
    update_color(doc, 1175, COLOR_BIRU_SALDO)
    if not quiet: print(f"  [OK] Tahap 7 (Summary Header): Awal={sawal_str} Masuk={dmasuk_str} Keluar={dkeluar_str} Akhir={sakhir_str}")

    # Row Nodes Definition (22 Rows)
    row_table_7395 = {
        1:  {'no_nodes': [(1518, '1'), (1523, None)], 'nom': {'2100': 1571, '150': 1576, '2206': 1586, 'txt': 1587, 'split': 1592}, 'sal': {'2100': 1596, '150': 1601, '2206': 1611, 'txt': 1612, 'split': 1617}, 'd_rec': 1657},
        2:  {'no_nodes': [(1758, '2')],               'nom': {'2100': 1762, '150': 1767, '2206': 1777, 'txt': 1778, 'split': None}, 'sal': {'2100': 1782, '150': 1787, '2206': 1797, 'txt': 1798, 'split': 1803}, 'd_rec': 1848},
        3:  {'no_nodes': [(1888, '3'), (1893, None)], 'nom': {'2100': 1933, '150': 1938, '2206': 1948, 'txt': 1949, 'split': None}, 'sal': {'2100': 1953, '150': 1958, '2206': 1968, 'txt': 1969, 'split': 1974}, 'd_rec': 2014},
        4:  {'no_nodes': [(2059, '4'), (2064, None)], 'nom': {'2100': 2099, '150': 2104, '2206': 2114, 'txt': 2115, 'split': None}, 'sal': {'2100': 2119, '150': 2124, '2206': 2134, 'txt': 2135, 'split': 2140}, 'd_rec': 2180},
        5:  {'no_nodes': [(2296, '5')],               'nom': {'2100': 2300, '150': 2305, '2206': 2315, 'txt': 2316, 'split': None}, 'sal': {'2100': 2320, '150': 2325, '2206': 2335, 'txt': 2336, 'split': None}, 'd_rec': 2376},
        6:  {'no_nodes': [(2416, '6'), (2421, None)], 'nom': {'2100': 2461, '150': 2466, '2206': 2476, 'txt': 2477, 'split': None}, 'sal': {'2100': 2481, '150': 2486, '2206': 2496, 'txt': 2497, 'split': 2502}, 'd_rec': 2542},
        7:  {'no_nodes': [(2582, '7'), (2587, None)], 'nom': {'2100': 2627, '150': 2632, '2206': 2642, 'txt': 2643, 'split': None}, 'sal': {'2100': 2647, '150': 2652, '2206': 2662, 'txt': 2663, 'split': 2668}, 'd_rec': 2708},
        8:  {'no_nodes': [(2803, '8')],               'nom': {'2100': 2807, '150': 2812, '2206': 2822, 'txt': 2823, 'split': None}, 'sal': {'2100': 2827, '150': 2832, '2206': 2842, 'txt': 2843, 'split': None}, 'd_rec': 2898},
        9:  {'no_nodes': [(2994, '9')],               'nom': {'2100': 2998, '150': 3003, '2206': 3013, 'txt': 3014, 'split': 3019}, 'sal': {'2100': 3023, '150': 3028, '2206': 3038, 'txt': 3039, 'split': None}, 'd_rec': 3079},
        10: {'no_nodes': [(3124, '1'), (3129, '0')],  'nom': {'2100': 3176, '150': 3181, '2206': 3191, 'txt': 3192, 'split': None}, 'sal': {'2100': 3196, '150': 3201, '2206': 3211, 'txt': 3212, 'split': None}, 'd_rec': 3257},
        11: {'no_nodes': [(4195, '11')],              'nom': {'2100': 4199, '150': 4204, '2206': 4214, 'txt': 4215, 'split': None}, 'sal': {'2100': 4219, '150': 4224, '2206': 4234, 'txt': 4235, 'split': 4240}, 'd_rec': 4280},
        12: {'no_nodes': [(4381, '12')],              'nom': {'2100': 4385, '150': 4390, '2206': 4400, 'txt': 4401, 'split': 4406}, 'sal': {'2100': 4410, '150': 4415, '2206': 4425, 'txt': 4426, 'split': 4431}, 'd_rec': 4471},
        13: {'no_nodes': [(4567, '13')],              'nom': {'2100': 4571, '150': 4576, '2206': 4586, 'txt': 4587, 'split': None}, 'sal': {'2100': 4591, '150': 4596, '2206': 4606, 'txt': 4607, 'split': 4612}, 'd_rec': 4652},
        14: {'no_nodes': [(4692, '1'), (4697, '4')],  'nom': {'2100': 4737, '150': 4742, '2206': 4752, 'txt': 4753, 'split': None}, 'sal': {'2100': 4757, '150': 4762, '2206': 4772, 'txt': 4773, 'split': None}, 'd_rec': 4818},
        15: {'no_nodes': [(4858, '1'), (4863, '5')],  'nom': {'2100': 4913, '150': 4918, '2206': 4928, 'txt': 4929, 'split': None}, 'sal': {'2100': 4933, '150': 4938, '2206': 4948, 'txt': 4949, 'split': None}, 'd_rec': 4999},
        16: {'no_nodes': [(5094, '16')],              'nom': {'2100': 5098, '150': 5103, '2206': 5113, 'txt': 5114, 'split': None}, 'sal': {'2100': 5118, '150': 5123, '2206': 5133, 'txt': 5134, 'split': 5139}, 'd_rec': 5184},
        17: {'no_nodes': [(5280, '17')],              'nom': {'2100': 5284, '150': 5289, '2206': 5299, 'txt': 5300, 'split': None}, 'sal': {'2100': 5304, '150': 5309, '2206': 5319, 'txt': 5320, 'split': None}, 'd_rec': 5370},
        18: {'no_nodes': [(5410, '1'), (5415, '8')],  'nom': {'2100': 5455, '150': 5460, '2206': 5470, 'txt': 5471, 'split': None}, 'sal': {'2100': 5475, '150': 5480, '2206': 5490, 'txt': 5491, 'split': 5496}, 'd_rec': 5536},
        19: {'no_nodes': [(5576, '1'), (5581, '9')],  'nom': {'2100': 5616, '150': 5621, '2206': 5631, 'txt': 5632, 'split': None}, 'sal': {'2100': 5636, '150': 5641, '2206': 5651, 'txt': 5652, 'split': 5657}, 'd_rec': 5697},
        20: {'no_nodes': [(5737, '2'), (5742, '0')],  'nom': {'2100': 5792, '150': 5797, '2206': 5807, 'txt': 5808, 'split': None}, 'sal': {'2100': 5812, '150': 5817, '2206': 5827, 'txt': 5828, 'split': 5833}, 'd_rec': 5873},
        21: {'no_nodes': [(5969, '2'), (5974, '1')],  'nom': {'2100': 5978, '150': 5983, '2206': 5993, 'txt': 5994, 'split': None}, 'sal': {'2100': 5998, '150': 6003, '2206': 6013, 'txt': 6014, 'split': None}, 'd_rec': 6059},
        22: {'no_nodes': [(6099, '2'), (6104, '2')],  'nom': {'2100': 6144, '150': 6149, '2206': 6159, 'txt': 6160, 'split': None}, 'sal': {'2100': 6164, '150': 6169, '2206': 6179, 'txt': 6180, 'split': None}, 'd_rec': 6230},
    }

    # July Dates Schedule
    jul_dates = [
        "01 Jul 2026", "01 Jul 2026", "02 Jul 2026", "02 Jul 2026", "03 Jul 2026",
        "04 Jul 2026", "04 Jul 2026", "05 Jul 2026", "05 Jul 2026", "06 Jul 2026",
        "08 Jul 2026", "09 Jul 2026", "10 Jul 2026", "11 Jul 2026", "12 Jul 2026",
        "13 Jul 2026", "14 Jul 2026", "14 Jul 2026", "15 Jul 2026", "15 Jul 2026",
        "16 Jul 2026", "31 Jul 2026"
    ]

    tx_list = cfg['transactions']
    for idx in range(1, 23):
        tx = tx_list[idx - 1]
        m = row_table_7395[idx]

        # 1. Row Number Normalization (1..22)
        for r_no_idx, r_no_val in m['no_nodes']:
            if r_no_val is not None:
                update_text_node(doc, r_no_idx, r_no_val)
            else:
                clean_split_node(doc, r_no_idx)

        # 2. Date Update (July 2026)
        update_text_node(doc, m['d_rec'], jul_dates[idx - 1])

        # 3. Nominal & Color & Right Align
        raw_nom = tx['nominal']
        nom_num = float(str(raw_nom).replace("+", "").replace("-", "").replace(".", "").replace(",", ".").replace(" ", "").strip() or 0.0)
        is_cr = raw_nom.startswith("+") or (not raw_nom.startswith("-") and tx.get('tipe') == 'CR')
        nom_fmt = f"{'+' if is_cr else '-'}{nom_num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        update_text_node(doc, m['nom']['txt'], nom_fmt)
        clean_split_node(doc, m['nom']['split'])
        w_nom = calc_text_width(nom_fmt)
        update_t2206(doc, m['nom']['2206'], w_nom)
        update_t2100(doc, m['nom']['2100'], TARGET_XR_NOMINAL_7395 - w_nom)
        update_color(doc, m['nom']['150'], COLOR_HIJAU_CR if is_cr else COLOR_HITAM_DB)

        # 4. Saldo & Right Align
        raw_sal = tx['saldo']
        sal_num = float(str(raw_sal).replace("+", "").replace("-", "").replace(".", "").replace(",", ".").replace(" ", "").strip() or 0.0)
        sal_fmt = f"{sal_num:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        
        update_text_node(doc, m['sal']['txt'], sal_fmt)
        clean_split_node(doc, m['sal']['split'])
        w_sal = calc_text_width(sal_fmt)
        update_t2206(doc, m['sal']['2206'], w_sal)
        update_t2100(doc, m['sal']['2100'], TARGET_XR_SALDO_7395 - w_sal)

    if not quiet: print(f"  [OK] Tahap 6 & 7: Updated all 22 Table Rows (Nominals, Saldos, Colors, Alignments, Dates & Sequential Numbers 1..22)")

if __name__ == '__main__':
    excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\Template_Pekerjaan_Xara_JUL.xlsx'
    cfg = parse_xara_excel_template(excel_path)
    
    xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar'
    doc = XarDocument(xar_path)
    print(f"Loaded {len(doc.records)} records from {xar_path}")
    
    execute_mandiri_3page_7395(doc, cfg)
    
    # Auto-sync size
    for r in doc.records:
        r['size'] = len(r['payload'])
        
    out_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0_output.xar'
    doc.save(out_xar)
    print(f"Saved to {out_xar}")
    
    # Reload and test integrity
    doc2 = XarDocument(out_xar)
    assert len(doc2.records) == len(doc.records)
    print("Verification SUCCESS! Record count match, zero errors.")
