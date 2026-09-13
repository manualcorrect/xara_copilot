import os
import struct
from xar_dom_engine import XarDocument

def execute_tahap7():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap6.xar'
    out_path_stage = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap7.xar'
    out_path_final = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_output.xar'

    print("=========================================================================")
    print("   PROJECT V2: TAHAP 7 - RINGKASAN & TABEL TRANSAKSI UTAMA (FINAL)")
    print(f"   Input File  : {in_path}")
    print(f"   Output File : {out_path_final}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Total records loaded: {total_recs_before}")

    GLYPH_WIDTHS = {
        '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
        '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
        '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
    }

    def calc_text_width(text):
        return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

    TARGET_XR_NOMINAL = 431355
    TARGET_XR_SALDO = 570390

    COLOR_HIJAU_CR = bytearray.fromhex('9f030000')
    COLOR_HITAM_DB = bytearray.fromhex('84010000')
    COLOR_BIRU_SALDO = bytearray.fromhex('e7040000')
    COLOR_ABU_AWAL = bytearray.fromhex('39030000')

    def update_text_node(rec_idx, text_str):
        p = bytearray(text_str.encode('utf-16le'))
        doc.records[rec_idx]['payload'] = p
        doc.records[rec_idx]['size'] = len(p)

    def clean_split_node(rec_idx):
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

    def update_t2206(rec_idx, w):
        if rec_idx:
            orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
            doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', w, orig[1], orig[2]))
            doc.records[rec_idx]['size'] = 12

    def update_t2100(rec_idx, x_left):
        if rec_idx:
            orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
            doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', x_left, orig[1], orig[2]))
            doc.records[rec_idx]['size'] = 12

    def update_color(rec_idx, color_payload):
        if rec_idx:
            doc.records[rec_idx]['payload'] = color_payload
            doc.records[rec_idx]['size'] = len(color_payload)

    # 1. Update Header Summary
    print("[*] 1. Updating Header Financial Summary...")
    # Saldo Awal: 1.020.834,00
    update_text_node(1091, "1.020.834,00 ")
    w_awal = calc_text_width("1.020.834,00 ")
    update_t2206(1085, w_awal)
    update_color(1086, COLOR_ABU_AWAL)

    # Dana Masuk: + 7.267.000,00
    update_text_node(1100, "+")
    update_text_node(1104, " 7.267.000,00")
    clean_split_node(1113)
    w_masuk = calc_text_width("+ 7.267.000,00")
    update_t2206(1095, w_masuk)
    update_color(1096, COLOR_HIJAU_CR)

    # Dana Keluar: - 6.358.330,00
    update_text_node(1131, "-6.358.330,00 ")
    w_keluar = calc_text_width("-6.358.330,00 ")
    update_t2206(1124, w_keluar)
    update_color(1125, COLOR_HITAM_DB)

    # Saldo Akhir: 1.929.504,00
    update_text_node(1143, "1.929.504,00")
    w_akhir = calc_text_width("1.929.504,00")
    update_t2206(1135, w_akhir)
    update_color(1137, COLOR_BIRU_SALDO)
    print("    -> Saldo Awal, Dana Masuk (+), Dana Keluar (-), Saldo Akhir updated cleanly.")

    # 2. Table Mutations (22 Rows)
    print("\n[*] 2. Updating 22 Rows of Table Mutations...")

    row_data = [
        # (r_num, nom_str, is_cr, saldo_str)
        (1, "-50.000,00", False, "970.834,00"),
        (2, "-300.000,00", False, "670.834,00"),
        (3, "+356.000,00", True, "1.026.834,00"),
        (4, "-8.000,00", False, "1.018.834,00"),
        (5, "-280.000,00", False, "738.834,00"),
        (6, "-726.830,00", False, "12.004,00"),
        (7, "-6.500,00", False, "5.504,00"),
        (8, "+41.000,00", True, "46.504,00"),
        (9, "-10.000,00", False, "36.504,00"),
        (10, "-11.500,00", False, "25.004,00"),
        (11, "+15.000,00", True, "40.004,00"),
        (12, "-15.000,00", False, "25.004,00"),
        (13, "+400.000,00", True, "425.004,00"),
        (14, "-400.000,00", False, "25.004,00"),
        (15, "+6.455.000,00", True, "6.480.004,00"),
        (16, "-5.500,00", False, "6.474.504,00"),
        (17, "-1.500.000,00", False, "4.974.504,00"),
        (18, "-390.000,00", False, "4.584.504,00"),
        (19, "-400.000,00", False, "4.184.504,00"),
        (20, "-1.000.000,00", False, "3.184.504,00"),
        (21, "-1.250.000,00", False, "1.934.504,00"),
        (22, "-5.000,00", False, "1.929.504,00")
    ]

    # Node mappings for rows 1 to 20:
    row_nodes = {
        1: {'s_txt': 1492, 's_2206': 1491, 's_2100': 1476, 'n_txt': 1512, 'n_split': 1517, 'n_2206': 1511, 'n_2100': 1496, 'n_150': 1501},
        2: {'s_txt': 1637, 's_2206': 1636, 's_2100': 1621, 'n_txt': 1657, 'n_split': None, 'n_2206': 1656, 'n_2100': 1641, 'n_150': 1646},
        3: {'s_txt': 1805, 's_2206': 1804, 's_2100': 1789, 'n_txt': 1825, 'n_split': 1830, 'n_2206': 1824, 'n_2100': 1809, 'n_150': 1814},
        4: {'s_txt': 1966, 's_2206': 1965, 's_2100': 1950, 'n_txt': 1986, 'n_split': 1991, 'n_2206': 1985, 'n_2100': 1970, 'n_150': 1975},
        5: {'s_txt': 2137, 's_2206': 2136, 's_2100': 2121, 'n_txt': 2157, 'n_split': 2162, 'n_2206': 2156, 'n_2100': 2141, 'n_150': 2146},
        6: {'s_txt': 2316, 's_2206': 2315, 's_2100': 2300, 'n_txt': 2336, 'n_split': 2341, 'n_2206': 2335, 'n_2100': 2320, 'n_150': 2325},
        7: {'s_txt': 2477, 's_2206': 2476, 's_2100': 2461, 'n_txt': 2497, 'n_split': 2502, 'n_2206': 2496, 'n_2100': 2481, 'n_150': 2486},
        8: {'s_txt': 2617, 's_2206': 2616, 's_2100': 2601, 'n_txt': 2637, 'n_split': None, 'n_2206': 2636, 'n_2100': 2621, 'n_150': 2626},
        9: {'s_txt': 2780, 's_2206': 2779, 's_2100': 2764, 'n_txt': 2800, 'n_split': None, 'n_2206': 2799, 'n_2100': 2784, 'n_150': 2789},
        10: {'s_txt': 2885, 's_2206': 2884, 's_2100': 2869, 'n_txt': 2908, 'n_pfx': 2904, 'n_split': 2917, 'n_2206': 2903, 'n_2100': 2889, 'n_150': 2894},
        11: {'s_txt': 4049, 's_2206': 4048, 's_2100': 4033, 'n_txt': 4069, 'n_split': None, 'n_2206': 4068, 'n_2100': 4053, 'n_150': 4058},
        12: {'s_txt': 4184, 's_2206': 4183, 's_2100': 4168, 'n_txt': 4204, 'n_split': None, 'n_2206': 4203, 'n_2100': 4188, 'n_150': 4193},
        13: {'s_txt': 4319, 's_2206': 4318, 's_2100': 4303, 'n_txt': 4339, 'n_split': 4344, 'n_2206': 4338, 'n_2100': 4323, 'n_150': 4328},
        14: {'s_txt': 4454, 's_2206': 4453, 's_2100': 4438, 'n_txt': 4474, 'n_split': None, 'n_2206': 4473, 'n_2100': 4458, 'n_150': 4463},
        15: {'s_txt': 4614, 's_2206': 4613, 's_2100': 4598, 'n_txt': 4634, 'n_split': None, 'n_2206': 4633, 'n_2100': 4618, 'n_150': 4623},
        16: {'s_txt': 4749, 's_2206': 4748, 's_2100': 4733, 'n_txt': 4769, 'n_split': None, 'n_2206': 4768, 'n_2100': 4753, 'n_150': 4758},
        17: {'s_txt': 4884, 's_2206': 4883, 's_2100': 4868, 'n_txt': 4904, 'n_split': None, 'n_2206': 4903, 'n_2100': 4888, 'n_150': 4893},
        18: {'s_txt': 5019, 's_2206': 5018, 's_2100': 5003, 'n_txt': 5039, 'n_split': None, 'n_2206': 5038, 'n_2100': 5023, 'n_150': 5028},
        19: {'s_txt': 5171, 's_2206': 5170, 's_2100': 5155, 'n_txt': 5191, 'n_split': 5196, 'n_2206': 5190, 'n_2100': 5175, 'n_150': 5180},
        20: {'s_txt': 5323, 's_2206': 5322, 's_2100': 5307, 'n_txt': 5343, 'n_split': 5348, 'n_2206': 5342, 'n_2100': 5327, 'n_150': 5332},
        21: {'s_txt': 5449, 's_2206': 5448, 's_2100': 5433, 'n_pfx': 5497, 'n_txt': 5502, 'n_150_1': 5499, 'n_150_2': 5504},
        22: {'s_txt': 5570, 's_2206': 5569, 's_2100': 5554, 'n_txt': 5618, 'n_150_1': 5613, 'n_150_2': 5620}
    }

    for r_num, nom_str, is_cr, saldo_str in row_data:
        m = row_nodes[r_num]

        # 1. Update Saldo
        update_text_node(m['s_txt'], saldo_str)
        w_saldo = calc_text_width(saldo_str)
        update_t2206(m['s_2206'], w_saldo)
        x_left_saldo = TARGET_XR_SALDO - w_saldo
        update_t2100(m['s_2100'], x_left_saldo)

        # 2. Update Nominal
        if r_num <= 20:
            if 'n_pfx' in m:
                # Row 10: prefix was '+'
                clean_split_node(m['n_pfx'])
            update_text_node(m['n_txt'], nom_str)
            if m.get('n_split'):
                clean_split_node(m['n_split'])
            w_nom = calc_text_width(nom_str)
            update_t2206(m['n_2206'], w_nom)
            x_left_nom = TARGET_XR_NOMINAL - w_nom
            update_t2100(m['n_2100'], x_left_nom)
            color_bytes = COLOR_HIJAU_CR if is_cr else COLOR_HITAM_DB
            update_color(m['n_150'], color_bytes)

        elif r_num == 21:
            # Row 21
            clean_split_node(m['n_pfx'])
            update_text_node(m['n_txt'], f"{nom_str} ")
            color_bytes = COLOR_HIJAU_CR if is_cr else COLOR_HITAM_DB
            update_color(m['n_150_1'], color_bytes)
            update_color(m['n_150_2'], color_bytes)

        elif r_num == 22:
            # Row 22
            update_text_node(m['n_txt'], f"{nom_str} ")
            color_bytes = COLOR_HIJAU_CR if is_cr else COLOR_HITAM_DB
            update_color(m['n_150_1'], color_bytes)
            update_color(m['n_150_2'], color_bytes)

        print(f"[*] Row {r_num:02d}: Nom = {nom_str:14s} ({'CR' if is_cr else 'DB'}) | Saldo = {saldo_str}")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path_stage and out_path_final
    doc.save(out_path_stage)
    doc.save(out_path_final)
    total_recs_after = len(doc.records)

    print(f"\n[SUCCESS] Tahap 7 completed successfully!")
    print(f"[*] Saved intermediate Tahap 7: {out_path_stage}")
    print(f"[*] Saved FINAL OUTPUT document: {out_path_final}")
    print(f"[*] Records verification: {total_recs_after} records (Zero-shift maintained: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap7()
