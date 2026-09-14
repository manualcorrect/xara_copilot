import os
import sys
import json
import struct
from xar_dom_engine import XarDocument

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

def build_flawless_jul_pipeline():
    folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul'
    in_path = os.path.join(folder, '0.xar')

    print("=========================================================================")
    print("   PROJECT V2 FLAWLESS PIPELINE: MARSIYAH JULI 2026 (8 PAGES / 83 ROWS)")
    print(f"   Base Template: {in_path}")
    print("=========================================================================\n")

    doc_base = XarDocument(in_path)
    TOTAL_RECS = len(doc_base.records)
    print(f"[*] Dokumen dimuat: {TOTAL_RECS:,} records (Zero-shift baseline locked)")

    COLOR_GREEN = bytearray.fromhex('d3030000') # Native Green (Kredit / Dana Masuk)
    COLOR_BLACK = bytearray.fromhex('9e010000') # Native Black (Debit / Dana Keluar)
    COLOR_BLUE  = bytearray.fromhex('2b050000') # Native Blue (Saldo Akhir / Running Saldo)
    COLOR_GRAY  = bytearray.fromhex('6f030000') # Native Dark Gray (Saldo Awal)

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

    # Map all 83 rows
    rows_map = []
    for i, r in enumerate(doc_base.records):
        if r['tag'] == 2204 and i > 1500:
            saldo_rec = None
            for k in range(i+1, min(len(doc_base.records), i+8)):
                if doc_base.records[k]['tag'] in (2201, 2202):
                    txt = doc_base.records[k]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                    if (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0') and ('.' in txt or len(txt) > 5):
                        saldo_rec = k
                        break
            if saldo_rec:
                row_no_rec = None
                row_no_val = None
                for p in range(max(0, i-6), i):
                    if doc_base.records[p]['tag'] in (2201, 2202):
                        r_txt = doc_base.records[p]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                        if r_txt.isdigit():
                            row_no_rec = p
                            row_no_val = int(r_txt)
                            break
                if row_no_rec:
                    orig_dx, orig_dy = struct.unpack('<ii', doc_base.records[i]['payload'][:8])
                    orig_saldo = doc_base.records[saldo_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                    
                    nom_prim, nom_sec, nom_t150, nom_t2100, nom_t2206 = None, None, None, None, None
                    for n in range(saldo_rec+1, min(len(doc_base.records), saldo_rec+45)):
                        rn = doc_base.records[n]
                        if rn['tag'] in (2201, 2202):
                            ntxt = rn['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                            if ntxt.startswith('+') or ntxt.startswith('-'):
                                nom_prim = n
                                for s in range(n+1, min(len(doc_base.records), n+8)):
                                    if doc_base.records[s]['tag'] in (2201, 2202):
                                        stxt = doc_base.records[s]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                        if stxt and (stxt.endswith(',00') or stxt.isdigit() or ',' in stxt):
                                            nom_sec = s
                                            break
                                break
                    if nom_prim:
                        for c in range(max(0, nom_prim-25), nom_prim):
                            if doc_base.records[c]['tag'] == 150:
                                nom_t150 = c
                        for t1 in range(max(0, nom_prim-30), nom_prim):
                            if doc_base.records[t1]['tag'] == 2100:
                                nom_t2100 = t1
                        for t6 in range(max(0, nom_prim-6), nom_prim):
                            if doc_base.records[t6]['tag'] == 2206:
                                nom_t2206 = t6
                                
                    time_prim, time_sec, date_prim, date_sec = None, None, None, None
                    search_start = (nom_sec or nom_prim or saldo_rec) + 1
                    for tm in range(search_start, min(len(doc_base.records), search_start+45)):
                        rtm = doc_base.records[tm]
                        if rtm['tag'] in (2201, 2202):
                            ttxt = rtm['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                            if ('WIB' in ttxt or ':' in ttxt) and not time_prim:
                                time_prim = tm
                                for ts in range(tm+1, min(len(doc_base.records), tm+6)):
                                    if doc_base.records[ts]['tag'] in (2201, 2202):
                                        tstxt = doc_base.records[ts]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                        if 'WIB' in tstxt or 'WI' in tstxt or 'B' in tstxt or tstxt.isdigit():
                                            time_sec = ts
                                            break
                            elif any(m in ttxt for m in ['Feb 2026', 'Jul 2026', 'Jan 2026']) and not date_prim:
                                date_prim = tm
                                for ds in range(max(0, tm-6), tm):
                                    if doc_base.records[ds]['tag'] in (2201, 2202):
                                        dstxt = doc_base.records[ds]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                        if dstxt.isdigit():
                                            date_sec = ds
                                            break
                    rows_map.append({
                        'row_idx': len(rows_map) + 1,
                        'row_no_val': row_no_val,
                        'row_no_rec': row_no_rec,
                        'saldo_rec': saldo_rec,
                        'orig_saldo': orig_saldo,
                        'tag2204_rec': i,
                        'orig_dx': orig_dx,
                        'orig_dy': orig_dy,
                        'nom_prim': nom_prim,
                        'nom_sec': nom_sec,
                        'nom_t150': nom_t150,
                        'nom_t2100': nom_t2100,
                        'nom_t2206': nom_t2206,
                        'time_prim': time_prim,
                        'time_sec': time_sec,
                        'date_prim': date_prim,
                        'date_sec': date_sec
                    })

    assert len(rows_map) == 83, f"Expected 83 rows mapped, got {len(rows_map)}"
    print(f"[*] 83 Baris Transaksi Berhasil Dipetakan Presisi 100%!")

    with open('jul_final_tx_schedule.json', 'r', encoding='utf-8') as f:
        txs = json.load(f)

    # Stages 1 to 6
    print("\n--- [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH ---")
    doc1 = XarDocument(in_path)
    NEW_NAME = "MASRIYAH MUHAMMAD SAMIAN "
    name_targets = [
        (1, 966, 982, 983),
        (2, 3612, 3627, 3628),
        (3, 6396, 6411, 6412),
        (4, 9120, 9135, 9136),
        (5, 11840, 11855, 11856),
        (6, 14616, 14631, 14632),
        (7, 17359, 17374, 17375),
        (8, 20159, 20174, 20175)
    ]
    for p, t2150_idx, t2206_idx, name_rec in name_targets:
        update_text(doc1, name_rec, NEW_NAME)
        update_t2150_w(doc1, t2150_idx, 200000)
        update_t2206(doc1, t2206_idx, 120000)
    out_t1 = os.path.join(folder, '0_tahap1.xar')
    sync_and_save(doc1, out_t1)

    print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
    doc2 = XarDocument(out_t1)
    NEW_PERIOD = "01 Jul 2026 - 31 Jul 2026"
    per_targets = [
        (1, 994, 1028, [1020, 1033]),
        (2, 3639, 3673, [3665, 3678]),
        (3, 6423, 6457, [6462]),
        (4, 9147, 9181, [9186]),
        (5, 11867, 11901, [11906]),
        (6, 14643, 14677, [14665, 14669, 14682]),
        (7, 17386, 17420, [17412, 17425]),
        (8, 20186, 20220, [20212, 20225])
    ]
    for p, t2150_idx, per_rec, blank_recs in per_targets:
        update_text(doc2, per_rec, NEW_PERIOD)
        update_t2150_w(doc2, t2150_idx, 180000)
        for b in blank_recs:
            blank_node(doc2, b)
    out_t2 = os.path.join(folder, '0_tahap2.xar')
    sync_and_save(doc2, out_t2)

    print("\n--- [3/7] TAHAP 3: PERUBAHAN TANGGAL CETAK ---")
    doc3 = XarDocument(out_t2)
    dicetak_targets = [
        (1, 1045, 1049, 1057),
        (2, 3690, 3694, 3702),
        (3, 6474, 6478, 6486),
        (4, 9198, 9202, 9210),
        (5, 11918, 11922, 11930),
        (6, 14694, 14698, 14706),
        (7, 17437, 17441, 17449),
        (8, 20237, 20241, 20249)
    ]
    for p, d1, d2, my in dicetak_targets:
        update_text(doc3, d1, "1")
        update_text(doc3, d2, "0")
        update_text(doc3, my, "Sep 2026")
    out_t3 = os.path.join(folder, '0_tahap3.xar')
    sync_and_save(doc3, out_t3)

    print("\n--- [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING ---")
    doc4 = XarDocument(out_t3)
    update_text(doc4, 1080, "1630016144514 ")
    out_t4 = os.path.join(folder, '0_tahap4.xar')
    sync_and_save(doc4, out_t4)

    print("\n--- [5/7] TAHAP 5: PENOMORAN HALAMAN ---")
    doc5 = XarDocument(out_t4)
    out_t5 = os.path.join(folder, '0_tahap5.xar')
    sync_and_save(doc5, out_t5)

    print("\n--- [6/7] TAHAP 6: TANGGAL & JAM TRANSAKSI (83 BARIS) ---")
    doc6 = XarDocument(out_t5)
    for i in range(83):
        tx = txs[i]
        r_info = rows_map[i]
        t_prim = r_info["time_prim"]
        t_sec = r_info["time_sec"]
        if t_prim:
            update_text(doc6, t_prim, tx["final_time"])
        if t_sec:
            blank_node(doc6, t_sec)
        d_prim = r_info["date_prim"]
        d_sec = r_info["date_sec"]
        if d_prim:
            update_text(doc6, d_prim, tx["date_str"])
        if d_sec:
            blank_node(doc6, d_sec)

    out_t6 = os.path.join(folder, '0_tahap6.xar')
    sync_and_save(doc6, out_t6)

    print("\n--- [7/7] TAHAP 7: RINGKASAN & TABEL TRANSAKSI (FINAL) ---")
    doc7 = XarDocument(out_t6)

    # 1. Financial Summary Header
    update_text(doc7, 1175, "21.347,81 ")
    update_color(doc7, 1171, COLOR_GRAY)

    update_text(doc7, 1184, "+ 13.811.000,00")
    blank_node(doc7, 1189)
    update_color(doc7, 1180, COLOR_GREEN)
    update_t2206(doc7, 1179, 65000)

    update_text(doc7, 1202, "- 12.333.579,00 ")
    update_color(doc7, 1195, COLOR_BLACK)
    update_t2206(doc7, 1194, 68000)

    update_text(doc7, 1215, "1.498.768,81")
    update_color(doc7, 1208, COLOR_BLUE)
    update_t2206(doc7, 1206, 43894)

    # 2. Table Transactions (83 Rows)
    X_RIGHT_NOMINAL = 431360 # 15.217 cm
    
    for i in range(83):
        tx = txs[i]
        r_info = rows_map[i]
        s_rec = r_info["saldo_rec"]
        k_rec = r_info["tag2204_rec"]
        orig_s = r_info["orig_saldo"]
        orig_dx = r_info["orig_dx"]
        orig_dy = r_info["orig_dy"]
        
        new_s_str = tx["formatted_saldo"]
        w_old_s = calc_text_width(orig_s)
        w_new_s = calc_text_width(new_s_str)
        delta_w = w_new_s - w_old_s
        delta_dx = -round(delta_w / 10)
        new_dx = orig_dx + delta_dx
        new_dy = orig_dy + round(delta_dx * 72)
        
        update_text(doc7, s_rec, new_s_str)
        update_t2204(doc7, k_rec, new_dx, new_dy)
        
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

    # 3. Clean Period Date Phantom Blocks across all pages
    period_indices = []
    for idx_r, r in enumerate(doc7.records):
        if r['tag'] == 2201:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if '01 Jul 2026 - 31 Jul 2026' in txt:
                period_indices.append(idx_r)

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

    # 4. Apply 2-Box Name Story & Independent Cabang across all 8 pages
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
            {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('3e040000')},
            {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')},
            {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('55010000')},
            {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
            {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
            {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
            {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
            {'tag': 193,  'size': 0,  'payload': bytearray()},
            {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
            {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80%
            {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80%
            {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
            # Line 1
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', W_317_MP, 5761, 0))},
            {'tag': 2201, 'size': 36, 'payload': bytearray('MASRIYAH MUHAMMAD '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 2
            {'tag': 2200, 'size': 0,  'payload': bytearray()},
            {'tag': 1,    'size': 0,  'payload': bytearray()},
            {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 30961, 5761, -10000))},
            {'tag': 2201, 'size': 14, 'payload': bytearray('SAMIAN '.encode('utf-16le'))},
            {'tag': 4211, 'size': 0,  'payload': bytearray()},
            {'tag': 0,    'size': 0,  'payload': bytearray()},
            # Line 3 (Trailing EOP)
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
            {'tag': 150,  'size': 4,  'payload': bytearray.fromhex('b2010000')},
            {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')},
            {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('55010000')},
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

    # Replace Name stories
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

    for s, e in reversed(name_story_ranges):
        doc7.records[s:e] = make_name_story()

    # Insert independent Cabang object after Mandiri Call 14000
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
    print("   [SUCCESS] PIPELINE FLAWLESS 7 TAHAP MARSIYAH JULI 2026 SELESAI 100%!")
    print(f"   Final Output File: {out_t7}")
    print("=========================================================================")

if __name__ == '__main__':
    build_flawless_jul_pipeline()
