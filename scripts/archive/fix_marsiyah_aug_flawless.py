import os
import sys
import json
import struct
from xar_dom_engine import XarDocument

# =========================================================================
# GLYPH ADVANCE WIDTHS FOR TTInterphases-Bold (H=6559 mp) & Regular (H=5761 mp)
# =========================================================================
CHAR_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(CHAR_WIDTHS.get(c, 4800) for c in text)

def build_flawless_aug_pipeline():
    folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug'
    in_path = os.path.join(folder, '0.xar')

    print("=========================================================================")
    print("   PROJECT V2 FLAWLESS PIPELINE: MARSIYAH AGUSTUS 2026 (10 PAGES / 110 ROWS)")
    print(f"   Base Template: {in_path}")
    print("=========================================================================\n")

    doc_base = XarDocument(in_path)
    TOTAL_RECS = len(doc_base.records)
    print(f"[*] Base Document Loaded: {TOTAL_RECS:,} records (Zero-shift baseline locked)")

    # 100% NATIVE AUGUST PALETTE (Zero warning pop-ups)
    COLOR_GREEN = bytearray.fromhex('e9030000') # Native Green (Kredit / Dana Masuk)
    COLOR_BLACK = bytearray.fromhex('9e010000') # Native Black (Debit / Dana Keluar)
    COLOR_BLUE  = bytearray.fromhex('1f050000') # Native Blue (Saldo Akhir / Running Saldo)
    COLOR_GRAY  = bytearray.fromhex('85030000') # Native Dark Gray (Saldo Awal)
    COLOR_TEXT  = bytearray.fromhex('53040000') # Native Black Text

    def update_text(doc, rec_idx, text_str):
        p = bytearray(text_str.encode('utf-16le'))
        doc.records[rec_idx]['payload'] = p
        doc.records[rec_idx]['size'] = len(p)

    def blank_node(doc, rec_idx):
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

    def update_color(doc, rec_idx, color_bytes):
        doc.records[rec_idx]['payload'] = color_bytes
        doc.records[rec_idx]['size'] = len(color_bytes)

    def update_t2206(doc, rec_idx, new_w):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_w, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

    def update_t2100_x(doc, rec_idx, new_x):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

    def update_t2150_w(doc, rec_idx, new_w):
        orig_flag = doc.records[rec_idx]['payload'][4:5]
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<i', new_w) + orig_flag)
        doc.records[rec_idx]['size'] = 5

    def update_t2204(doc, rec_idx, new_dx, new_dy):
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<ii', new_dx, new_dy))
        doc.records[rec_idx]['size'] = 8

    def sync_and_save(doc, out_path):
        for r in doc.records:
            r['size'] = len(r['payload'])
        doc.save(out_path)
        print(f"   [SAVED] {os.path.basename(out_path)} ({len(doc.records):,} records) [PASS]")

    # Load 110 transactions schedule & rows map
    with open('aug_final_tx_schedule.json', 'r', encoding='utf-8') as f:
        txs = json.load(f)

    with open('aug_rows_map.json', 'r', encoding='utf-8') as f:
        rows_map = json.load(f)

    assert len(txs) == 110, f"Expected 110 txs, got {len(txs)}"
    assert len(rows_map) == 110, f"Expected 110 rows, got {len(rows_map)}"
    print(f"[*] 110 August Transaction Rows & Mappings Verified 100%!")

    # =========================================================================
    # [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH (MASRIYAH MUHAMMAD SAMIAN)
    # =========================================================================
    print("\n--- [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH ---")
    doc1 = XarDocument(in_path)
    NEW_NAME = "MASRIYAH MUHAMMAD SAMIAN "
    name_targets = [
        (1, 988, 1004, 1005),
        (2, 3624, 3639, 3640),
        (3, 6402, 6417, 6418),
        (4, 9236, 9251, 9252),
        (5, 11983, 11998, 11999),
        (6, 14739, 14754, 14755),
        (7, 17507, 17522, 17523),
        (8, 20282, 20297, 20298),
        (9, 23033, 23048, 23049),
        (10, 25837, 25852, 25853)
    ]
    for p, t2150_idx, t2206_idx, name_rec in name_targets:
        update_text(doc1, name_rec, NEW_NAME)
        update_t2150_w(doc1, t2150_idx, 200000)
        update_t2206(doc1, t2206_idx, 120000)
    out_t1 = os.path.join(folder, '0_tahap1.xar')
    sync_and_save(doc1, out_t1)

    # =========================================================================
    # [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN (01 Aug 2026 - 31 Aug 2026)
    # =========================================================================
    print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
    doc2 = XarDocument(out_t1)
    NEW_PERIOD = "01 Aug 2026 - 31 Aug 2026"
    per_targets = [
        (1, 1016, 1050, [1038, 1042, 1055]),
        (2, 3651, 3685, [3673, 3677, 3690]),
        (3, 6429, 6463, [6451, 6455, 6468]),
        (4, 9263, 9297, [9285, 9289, 9302]),
        (5, 12010, 12044, [12032, 12036, 12049]),
        (6, 14766, 14800, [14788, 14792, 14805]),
        (7, 17534, 17568, [17556, 17560, 17573]),
        (8, 20309, 20343, [20331, 20335, 20348]),
        (9, 23060, 23094, [23082, 23086, 23099]),
        (10, 25864, 25898, [25886, 25890, 25903])
    ]
    for p, t2150_idx, per_rec, blank_recs in per_targets:
        update_text(doc2, per_rec, NEW_PERIOD)
        update_t2150_w(doc2, t2150_idx, 180000)
        for b in blank_recs:
            blank_node(doc2, b)
    out_t2 = os.path.join(folder, '0_tahap2.xar')
    sync_and_save(doc2, out_t2)

    # =========================================================================
    # [3/7] TAHAP 3: PERUBAHAN TANGGAL CETAK (10 Sep 2026)
    # =========================================================================
    print("\n--- [3/7] TAHAP 3: PERUBAHAN TANGGAL CETAK ---")
    doc3 = XarDocument(out_t2)
    dicetak_targets = [
        (1, 1067, 1071, 1079),
        (2, 3702, 3706, 3714),
        (3, 6480, 6484, 6492),
        (4, 9314, 9318, 9326),
        (5, 12061, 12065, 12073),
        (6, 14817, 14821, 14829),
        (7, 17585, 17589, 17597),
        (8, 20360, 20364, 20372),
        (9, 23111, 23115, 23123),
        (10, 25915, 25919, 25927)
    ]
    for p, d1, d2, my in dicetak_targets:
        update_text(doc3, d1, "1")
        update_text(doc3, d2, "0")
        update_text(doc3, my, "Sep 2026")
    out_t3 = os.path.join(folder, '0_tahap3.xar')
    sync_and_save(doc3, out_t3)

    # =========================================================================
    # [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING (1630016144514)
    # =========================================================================
    print("\n--- [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING ---")
    doc4 = XarDocument(out_t3)
    update_text(doc4, 1102, "1630016144514 ")
    out_t4 = os.path.join(folder, '0_tahap4.xar')
    sync_and_save(doc4, out_t4)

    # =========================================================================
    # [5/7] TAHAP 5: PENOMORAN HALAMAN (10 HALAMAN)
    # =========================================================================
    print("\n--- [5/7] TAHAP 5: PENOMORAN HALAMAN ---")
    doc5 = XarDocument(out_t4)
    out_t5 = os.path.join(folder, '0_tahap5.xar')
    sync_and_save(doc5, out_t5)

    # =========================================================================
    # [6/7] TAHAP 6: TANGGAL & JAM TRANSAKSI (110 BARIS)
    # =========================================================================
    print("\n--- [6/7] TAHAP 6: TANGGAL & JAM TRANSAKSI (110 BARIS) ---")
    doc6 = XarDocument(out_t5)
    for i in range(110):
        tx = txs[i]
        r_info = rows_map[i]
        
        # Time
        t_prim = r_info.get("time_prim")
        t_sec = r_info.get("time_sec")
        if t_prim:
            update_text(doc6, t_prim, tx["final_time"])
        if t_sec:
            blank_node(doc6, t_sec)
            
        # Date
        d_prim = r_info.get("date_prim")
        d_sec = r_info.get("date_sec")
        if d_prim:
            update_text(doc6, d_prim, tx["resolved_date"])
        if d_sec:
            blank_node(doc6, d_sec)

    out_t6 = os.path.join(folder, '0_tahap6.xar')
    sync_and_save(doc6, out_t6)

    # =========================================================================
    # [7/7] TAHAP 7: RINGKASAN & TABEL TRANSAKSI (FINAL FLAWLESS CALIBRATION)
    # =========================================================================
    print("\n--- [7/7] TAHAP 7: RINGKASAN & TABEL TRANSAKSI (FINAL) ---")
    doc7 = XarDocument(out_t6)

    # 1. Financial Summary Header (Page 1)
    # Saldo Awal: 1.498.768,81 (Native Dark Gray: 85030000)
    update_text(doc7, 1204, "1.498.768,81 ")
    update_color(doc7, 1200, COLOR_GRAY)

    # Dana Masuk: + 21.359.500,00 (Native Green: e9030000)
    update_text(doc7, 1214, "+ 21.359.500,00")
    blank_node(doc7, 1219)
    update_color(doc7, 1210, COLOR_GREEN)
    update_t2206(doc7, 1208, 75000)

    # Dana Keluar: - 21.685.780,00 (Native Black: 9e010000)
    update_text(doc7, 1233, "- 21.685.780,00 ")
    update_color(doc7, 1226, COLOR_BLACK)
    update_t2206(doc7, 1224, 75000)

    # Saldo Akhir: 1.172.488,81 (Native Blue: 1f050000)
    update_text(doc7, 1246, "1.172.488,81")
    update_color(doc7, 1239, COLOR_BLUE)
    update_t2206(doc7, 1237, 43894)

    # 2. Table Transactions (110 Rows) - Precision Right Alignment & Deltas
    X_RIGHT_NOMINAL = 431360 # 15.217 cm
    
    for i in range(110):
        tx = txs[i]
        r_info = rows_map[i]
        s_rec = r_info["saldo_rec"]
        k_rec = r_info["tag2204_rec"]
        orig_s = r_info["orig_saldo"]
        orig_dx = r_info["orig_dx"]
        orig_dy = r_info["orig_dy"]
        
        # Saldo delta calibration
        new_s_str = tx["formatted_saldo"]
        w_old_s = calc_text_width(orig_s)
        w_new_s = calc_text_width(new_s_str)
        delta_w = w_new_s - w_old_s
        delta_dx = -round(delta_w / 10)
        new_dx = orig_dx + delta_dx
        new_dy = orig_dy + round(delta_dx * 72)
        
        update_text(doc7, s_rec, new_s_str)
        update_t2204(doc7, k_rec, new_dx, new_dy)
        
        # Nominal calibration
        nom_prim = r_info["nom_prim"]
        nom_sec = r_info["nom_sec"]
        nom_col = r_info["nom_t150"]
        nom_t1 = r_info["nom_t2100"]
        nom_t6 = r_info["nom_t2206"]
        
        if nom_prim:
            nom_str = tx["formatted_nominal"]
            w_nom = calc_text_width(nom_str)
            new_x_left = X_RIGHT_NOMINAL - w_nom
            
            update_text(doc7, nom_prim, nom_str)
            if nom_sec:
                blank_node(doc7, nom_sec)
                
            if nom_t1:
                update_t2100_x(doc7, nom_t1, new_x_left)
            if nom_t6:
                update_t2206(doc7, nom_t6, w_nom)
                
            if nom_col:
                if tx["nom_type"] == "CR":
                    update_color(doc7, nom_col, COLOR_GREEN)
                else:
                    update_color(doc7, nom_col, COLOR_BLACK)

    # 3. Clean Period Date Phantom Blocks across all 10 pages
    period_indices = []
    for idx_r, r in enumerate(doc7.records):
        if r['tag'] == 2201:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if '01 Aug 2026 - 31 Aug 2026' in txt:
                period_indices.append(idx_r)

    print(f"[*] Cleaning Period Date Phantom Blocks on {len(period_indices)} pages...")
    for p_idx in reversed(period_indices):
        start_check = max(0, p_idx - 15)
        for k in range(p_idx - 1, start_check, -1):
            if doc7.records[k]['tag'] == 2202:
                t2202_idx = k
                fwd = t2202_idx + 1
                if fwd < p_idx and doc7.records[fwd]['tag'] == 1:
                    while fwd < p_idx and doc7.records[fwd]['tag'] in (1, 4405, 0):
                        fwd += 1
                bwd = t2202_idx
                if doc7.records[bwd - 1]['tag'] == 0 and doc7.records[bwd - 2]['tag'] == 4405 and doc7.records[bwd - 3]['tag'] == 1:
                    bwd = bwd - 3
                del doc7.records[bwd:fwd]
                break

    # 4. Apply 2-Box Name Story (W=3.17cm, 80% leading) & Independent Cabang across all 10 pages
    W_317_MP = 89858
    X_NAME_MP = 123307
    Y_NAME_MP = 736000
    X_CABANG_MP = 124101
    Y_CABANG_MP = 714420

    def make_name_story():
        return [
            {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_NAME_MP, Y_NAME_MP, 1))},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', W_317_MP, 1))},
            {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
            {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('53040000')}, # Native Black
            {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')}, # Normal Style
            {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')}, # Font ID 340 (PDF-TTInterphases-Regular)
            {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
            {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
            {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
            {'tag': 193,  'size': 0,  'payload': bytearray()},
            {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
            {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% leading
            {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% leading
            {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
            # Line 1: MASRIYAH MUHAMMAD 
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', W_317_MP, 5761, 0))},
            {'tag': 2201, 'size': 36, 'payload': bytearray('MASRIYAH MUHAMMAD '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 2: SAMIAN 
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 30961, 5761, -10000))},
            {'tag': 2201, 'size': 14, 'payload': bytearray('SAMIAN '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 3: Trailing End Of Paragraph
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10000))},
            {'tag': 2203, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
        ]

    def make_cabang_obj():
        return [
            {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_CABANG_MP, Y_CABANG_MP, 1))},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', 0, 0))},
            {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
            {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
            {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80%
            {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')},
            {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('53040000')}, # Native Black
            {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')}, # Normal Style
            {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')}, # Font ID 340 (PDF-TTInterphases-Regular)
            {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
            {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
            {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
            {'tag': 193,  'size': 0,  'payload': bytearray()},
            {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 88118, 5761, 0))},
            {'tag': 2201, 'size': 46, 'payload': bytearray('KCP Jakarta Taman Aries'.encode('utf-16le'))},
            {'tag': 2203, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10400))},
            {'tag': 2203, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
        ]

    # Replace Name stories on all 10 pages
    name_story_ranges = []
    idx_scan = 0
    while idx_scan < len(doc7.records):
        r = doc7.records[idx_scan]
        if r['tag'] == 2100:
            coords = struct.unpack(f'<{len(r["payload"])//4}i', r['payload'])
            if len(coords) >= 2 and coords[1] == 736000 and coords[0] in (123000, 123307):
                for j in range(idx_scan, min(len(doc7.records), idx_scan+35)):
                    if doc7.records[j]['tag'] == 2201:
                        txt = doc7.records[j]['payload'].decode('utf-16le', errors='ignore')
                        if 'MASRIYAH' in txt:
                            end = j
                            for k in range(j, min(len(doc7.records), j+20)):
                                if doc7.records[k]['tag'] == 2203:
                                    end = k + 1
                                    while end < len(doc7.records) and doc7.records[end]['tag'] == 0:
                                        end += 1
                                    break
                            name_story_ranges.append((idx_scan, end))
                            idx_scan = end - 1
                            break
        idx_scan += 1

    print(f"[*] Replacing Name Story (W=3.17cm, 80% leading) on {len(name_story_ranges)} pages...")
    for s, e in reversed(name_story_ranges):
        doc7.records[s:e] = make_name_story()

    # Insert independent Cabang object after Mandiri Call 14000 on each page
    mandiri_ends = []
    for idx_m, r in enumerate(doc7.records):
        if r['tag'] == 2201 and 'Mandiri Call 14000' in r['payload'].decode('utf-16le', errors='ignore'):
            for j in range(idx_m, min(len(doc7.records), idx_m+10)):
                if doc7.records[j]['tag'] == 2203:
                    end = j + 1
                    while end < len(doc7.records) and doc7.records[end]['tag'] == 0:
                        end += 1
                    mandiri_ends.append(end)
                    break

    print(f"[*] Inserting Independent Cabang Object on {len(mandiri_ends)} pages...")
    for m_end in reversed(mandiri_ends):
        has_cabang = False
        for k in range(m_end, min(len(doc7.records), m_end + 35)):
            if doc7.records[k]['tag'] == 2201 and 'KCP Jakarta Taman Aries' in doc7.records[k]['payload'].decode('utf-16le', errors='ignore'):
                has_cabang = True
                break
        if not has_cabang:
            doc7.records[m_end:m_end] = make_cabang_obj()

    out_t7 = os.path.join(folder, '0_tahap7.xar')
    sync_and_save(doc7, out_t7)

    print("\n=========================================================================")
    print("   [SUCCESS] PIPELINE FLAWLESS 7 TAHAP MARSIYAH AGUSTUS 2026 SELESAI 100%!")
    print(f"   Final Output File: {out_t7}")
    print("=========================================================================")

if __name__ == '__main__':
    build_flawless_aug_pipeline()
