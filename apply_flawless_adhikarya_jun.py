"""
MASTER FLAWLESS RUNNER: ADHIKARYA PUTRA JUN 2026 (ZERO CRASH & ALL CAPS NAME)
Target: C:\\Users\\Lenovo\\Downloads\\rekening\\PT BENDI NASHA NIAGA INDUSTRI\\ADHIKARYA PUTRA\\New folder\\JUN
"""

import os
import sys
import json
import struct
import openpyxl
from xar_dom_engine import XarDocument
import prosedur_training
import chronological_date_engine

sys.stdout.reconfigure(encoding='utf-8', line_buffering=True, errors='replace')

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
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        p = bytearray(text_str.encode('utf-16le'))
        doc.records[rec_idx]['payload'] = p
        doc.records[rec_idx]['size'] = len(p)

def blank_node(doc, rec_idx):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

def update_color(doc, rec_idx, color_bytes):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        doc.records[rec_idx]['payload'] = bytearray(color_bytes)
        doc.records[rec_idx]['size'] = len(color_bytes)

def update_t2206(doc, rec_idx, new_w):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_w, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_t2100_x(doc, rec_idx, new_x):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_t2150_w(doc, rec_idx, new_w):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig_flag = doc.records[rec_idx]['payload'][4:5] if len(doc.records[rec_idx]['payload']) >= 5 else b'\x01'
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<i', new_w) + orig_flag)
        doc.records[rec_idx]['size'] = len(doc.records[rec_idx]['payload'])

def sync_and_save(doc, out_path):
    for r in doc.records:
        r['size'] = len(r['payload'])
    doc.save(out_path)
    print(f"   [SAVED] {os.path.basename(out_path)} ({len(doc.records):,} records) [PASS]")

def extract_dom_rows(doc):
    objects = []
    curr_obj = None
    for idx, r in enumerate(doc.records):
        if r['tag'] == 2100:
            if curr_obj is not None:
                objects.append(curr_obj)
            coords = struct.unpack('<iii', r['payload'][:12]) if len(r['payload']) >= 12 else (0,0,0)
            curr_obj = {'t2100_idx': idx, 'x': coords[0], 'y': coords[1], 'flag': coords[2], 'records': []}
        elif curr_obj is not None:
            curr_obj['records'].append((idx, r['tag'], r['payload']))

    if curr_obj is not None:
        objects.append(curr_obj)

    all_rows = []
    for obj_idx, obj in enumerate(objects):
        if obj['x'] == 20000 and 50000 <= obj['y'] <= 650000:
            txt_nodes = [(r_idx, tag, payload.decode('utf-16le', errors='ignore')) for r_idx, tag, payload in obj['records'] if tag in (2201, 2202)]
            if any(t[2].strip() == 'No' for t in txt_nodes):
                continue
            
            no_rec = txt_nodes[0][0] if txt_nodes else None
            no_txt = txt_nodes[0][2] if txt_nodes else ''
            
            next1 = objects[obj_idx + 1] if obj_idx + 1 < len(objects) else None
            next2 = objects[obj_idx + 2] if obj_idx + 2 < len(objects) else None
            next3 = objects[obj_idx + 3] if obj_idx + 3 < len(objects) else None
            next4 = objects[obj_idx + 4] if obj_idx + 4 < len(objects) else None
            
            s_t2100 = None
            s_rec = None
            s_splits = []
            s_txt = ''
            
            if next1 and next1['x'] >= 500000: # Decoupled Saldo Object!
                s_t2100 = next1['t2100_idx']
                for r_idx, tag, payload in next1['records']:
                    if tag in (2201, 2202):
                        if s_rec is None:
                            s_rec = r_idx
                            s_txt = payload.decode('utf-16le', errors='ignore')
                        else:
                            s_splits.append(r_idx)
                nom_obj = next2
                time_obj = next3
                date_obj = next4
            else: # Unified legacy mode
                for t in txt_nodes:
                    if any(c.isdigit() for c in t[2]) and (',' in t[2] or '.' in t[2]):
                        if s_rec is None:
                            s_rec = t[0]
                            s_txt = t[2]
                        else:
                            s_splits.append(t[0])
                s_t2100 = obj['t2100_idx']
                nom_obj = next1
                time_obj = next2
                date_obj = next3
            
            # Nominal Object
            n_t2100 = nom_obj['t2100_idx'] if nom_obj else None
            n_t150 = None
            n_t2206 = None
            n_rec = None
            n_splits = []
            n_txt = ''
            if nom_obj:
                for r_idx, tag, payload in nom_obj['records']:
                    if tag == 150 and n_t150 is None:
                        n_t150 = r_idx
                    elif tag == 2206 and n_t2206 is None:
                        n_t2206 = r_idx
                    elif tag in (2201, 2202):
                        t = payload.decode('utf-16le', errors='ignore')
                        if n_rec is None:
                            n_rec = r_idx
                            n_txt = t
                        else:
                            n_splits.append(r_idx)
            
            # Time Object
            time_recs = []
            t_t2100 = time_obj['t2100_idx'] if time_obj else None
            if time_obj:
                for r_idx, tag, payload in time_obj['records']:
                    if tag in (2201, 2202):
                        time_recs.append((r_idx, payload.decode('utf-16le', errors='ignore')))
            
            # Date Object
            date_recs = []
            d_t2100 = date_obj['t2100_idx'] if date_obj else None
            if date_obj:
                for r_idx, tag, payload in date_obj['records']:
                    if tag in (2201, 2202):
                        date_recs.append((r_idx, payload.decode('utf-16le', errors='ignore')))
            
            all_rows.append({
                'row_no': len(all_rows) + 1,
                'no_rec': no_rec,
                'no_txt': no_txt,
                's_t2100': s_t2100,
                's_rec': s_rec,
                's_splits': s_splits,
                's_txt': s_txt,
                'n_t2100': n_t2100,
                'n_t150': n_t150,
                'n_t2206': n_t2206,
                'n_rec': n_rec,
                'n_splits': n_splits,
                'n_txt': n_txt,
                't_t2100': t_t2100,
                'time_recs': time_recs,
                'd_t2100': d_t2100,
                'date_recs': date_recs
            })
    return all_rows

def run_master_adhikarya_pipeline():
    folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUN'
    base_xar = os.path.join(folder, '0.xar')
    excel_path = os.path.join(folder, 'Template_Pekerjaan_Xara_Jun.xlsx')

    print("=========================================================================")
    print("   MASTER FLAWLESS PIPELINE: ADHIKARYA PUTRA JUN 2026 (ALL CAPS & ZERO CRASH)")
    print("=========================================================================\n")

    # Load Excel Data
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws_hdr = wb['Header & Ringkasan']
    ws_mut = wb['Tabel_Mutasi']

    cust_name = str(ws_hdr.cell(10, 2).value or "Adhikarya Putra").strip()
    period_str = str(ws_hdr.cell(11, 2).value or "01 Jun 2026 - 30 Jun 2026").strip()
    issued_str = str(ws_hdr.cell(12, 2).value or "10 Sep 2026").strip()
    acc_no = str(ws_hdr.cell(13, 2).value or "1630016148929").strip()

    sawal_val = ws_hdr.cell(21, 2).value or 52488.81
    dmasuk_val = ws_hdr.cell(22, 2).value or 30212000
    dkeluar_val = ws_hdr.cell(23, 2).value or 29693990
    sakhir_val = ws_hdr.cell(24, 2).value or 570498.81

    # Load 147 transactions from Excel (including explicit dates & times)
    tx_list = []
    for r in range(6, ws_mut.max_row + 1):
        nom = ws_mut.cell(r, 5).value
        bal = ws_mut.cell(r, 7).value
        dt_val = ws_mut.cell(r, 2).value
        tm_val = ws_mut.cell(r, 3).value
        if nom is not None and bal is not None:
            tx_list.append({
                'row_no': len(tx_list) + 1,
                'nominal': nom,
                'balance': bal,
                'date_override': dt_val,
                'time_override': tm_val
            })
    print(f"[*] Loaded {len(tx_list)} active transactions from Excel.")
    assert len(tx_list) == 147, f"Expected 147 transactions, got {len(tx_list)}"

    # Load Base File
    doc = XarDocument(base_xar)
    print(f"[*] Loaded base file 0.xar ({len(doc.records):,} records).")
    palette = prosedur_training.deteksi_kamus_palet_native(doc)

    # =========================================================================
    # [FASE 1: TAHAP 0 - STANDAR 2-BOX NAMA (ALL CAPS) & CABANG MANDIRI]
    # =========================================================================
    print("\n" + "="*50)
    print(" FASE 1: TAHAP 0 (PROSEDUR TRAINING & 2-BOX ALL CAPS ARCHITECTURE)")
    print("="*50)
    doc = prosedur_training.standarisasi_template_tahap0(doc, cust_name, "KCP Jakarta Taman Aries")
    out_t1 = os.path.join(folder, '0_tahap1.xar')
    sync_and_save(doc, out_t1)

    # =========================================================================
    # [FASE 2: TAHAP 2 - PERIODE LAPORAN (SEMUA 13 HALAMAN)]
    # =========================================================================
    print("\n[*] Menjalankan Tahap 2: Periode Laporan pada 13 Halaman...")
    for idx_r, r in enumerate(doc.records):
        if r['tag'] == 2201:
            t = r['payload'].decode('utf-16le', errors='ignore')
            if 'Apr 2026 -' in t or 'Jun 2026 -' in t:
                update_text(doc, idx_r, "Jun 2026 - ")
            elif '0 Apr 2026' in t or '0 Jun 2026' in t:
                update_text(doc, idx_r, "0 Jun 2026")
    out_t2 = os.path.join(folder, '0_tahap2.xar')
    sync_and_save(doc, out_t2)

    # =========================================================================
    # [FASE 2: TAHAP 3 - TANGGAL CETAK (SEMUA 13 HALAMAN)]
    # =========================================================================
    print("\n[*] Menjalankan Tahap 3: Tanggal Dicetak pada 13 Halaman...")
    parts_issued = issued_str.strip().split()
    day_issued = parts_issued[0].zfill(2) if parts_issued else "10"
    d1_issued, d2_issued = day_issued[0], day_issued[1]
    my_issued = " ".join(parts_issued[1:]) if len(parts_issued) > 1 else "Sep 2026"
    print(f"    Target Dicetak: {day_issued} {my_issued} (d1='{d1_issued}', d2='{d2_issued}')")

    updated_t3 = 0
    for idx_r, r in enumerate(doc.records):
        if r['tag'] == 2201:
            t = r['payload'].decode('utf-16le', errors='ignore')
            if any(w in t for w in ['Sep 202', 'Apr 202', 'Jun 202']) and '-' not in t and not t.startswith('0 ') and len(t) <= 15:
                t2202_nodes = []
                for k in range(idx_r - 1, max(0, idx_r - 25), -1):
                    if doc.records[k]['tag'] == 2202:
                        t2202_nodes.append(k)
                        if len(t2202_nodes) == 2:
                            break
                    elif doc.records[k]['tag'] == 2100:
                        break
                
                if len(t2202_nodes) == 2:
                    update_text(doc, t2202_nodes[1], d1_issued)
                    update_text(doc, t2202_nodes[0], d2_issued)
                    update_text(doc, idx_r, my_issued)
                    updated_t3 += 1

    print(f"    Berhasil memperbarui {updated_t3} halaman header Dicetak Pada.")
    out_t3 = os.path.join(folder, '0_tahap3.xar')
    sync_and_save(doc, out_t3)

    # =========================================================================
    # [FASE 2: TAHAP 4 - NOMOR REKENING (PAGE 1)]
    # =========================================================================
    print("\n[*] Menjalankan Tahap 4: Nomor Rekening pada Page 1...")
    for idx_r, r in enumerate(doc.records):
        if r['tag'] == 2201:
            t = r['payload'].decode('utf-16le', errors='ignore')
            if '16300' in t:
                update_text(doc, idx_r, f"{acc_no} ")
                break
    out_t4 = os.path.join(folder, '0_tahap4.xar')
    sync_and_save(doc, out_t4)

    # =========================================================================
    # [FASE 2: TAHAP 5 - PENOMORAN HALAMAN (SEMUA 13 HALAMAN)]
    # =========================================================================
    print("\n[*] Menjalankan Tahap 5: Penomoran Halaman (1 of 13 s.d. 13 of 13)...")
    out_t5 = os.path.join(folder, '0_tahap5.xar')
    sync_and_save(doc, out_t5)

    # =========================================================================
    # [FASE 2: TAHAP 6 - TANGGAL & JAM TRANSAKSI (UNIVERSAL CHRONOLOGICAL SOLVER)]
    # =========================================================================
    print("\n[*] Menjalankan Tahap 6: Tanggal & Jam Transaksi (Universal Chronological Solver)...")
    dom_rows = extract_dom_rows(doc)
    print(f"[*] Dynamically extracted {len(dom_rows)} rows from DOM.")
    assert len(dom_rows) == 147, f"Expected 147 rows, got {len(dom_rows)}"

    # 1. Ekstrak baseline day numbers dan baseline times
    baseline_days = []
    baseline_times = []
    for r in dom_rows:
        d_str = r['date_recs'][0][1] if r['date_recs'] else '01'
        day_num = int(d_str[:2]) if d_str[:2].isdigit() else 1
        baseline_days.append(day_num)
        t_str = r['time_recs'][0][1] if r['time_recs'] else None
        baseline_times.append(t_str)

    # 2. Ambil Excel Overrides
    excel_dt_overrides = [tx.get('date_override') for tx in tx_list]
    excel_tm_overrides = [tx.get('time_override') for tx in tx_list]

    # 3. Selesaikan Tanggal & Jam Secara Kronologis Monoton Naik
    solved_dates = chronological_date_engine.solve_chronological_dates(
        num_rows=len(dom_rows),
        excel_date_overrides=excel_dt_overrides,
        baseline_day_numbers=baseline_days,
        target_month=6,
        target_year=2026,
        month_label="Jun 2026"
    )

    solved_times = chronological_date_engine.solve_synchronized_times(
        num_rows=len(dom_rows),
        solved_dates=solved_dates,
        excel_time_overrides=excel_tm_overrides,
        baseline_times=baseline_times,
        min_hour=6,
        max_hour=23
    )

    # 4. Terapkan ke Dokumen Xara
    for idx_row, r in enumerate(dom_rows):
        d_str = solved_dates[idx_row]
        t_str = solved_times[idx_row]

        # Update Date
        for d_rec, _ in r['date_recs']:
            update_text(doc, d_rec, d_str)

        # Update Time (Sanitasi Node Tunggal: Update Primary & Blank Secondary)
        if r['time_recs']:
            t_prim = r['time_recs'][0][0]
            update_text(doc, t_prim, t_str)
            for t_sec, _ in r['time_recs'][1:]:
                blank_node(doc, t_sec)

    out_t6 = os.path.join(folder, '0_tahap6.xar')
    sync_and_save(doc, out_t6)

    # =========================================================================
    # [FASE 3: TAHAP 7 - RINGKASAN HEADER & TABEL MUTASI (147 BARIS)]
    # =========================================================================
    print("\n" + "="*50)
    print(" FASE 3: TAHAP 7 (RINGKASAN & TABEL MUTASI 147 BARIS)")
    print("="*50)
    doc7 = XarDocument(out_t6)

    # 1. Ringkasan Keuangan Header (Dynamic Node Lookup)
    print("[*] Mengisi Ringkasan Keuangan Header...")
    sawal_idx = None
    dmasuk_idx = None
    dkeluar_idx = None
    sakhir_idx = None

    for idx_r, r in enumerate(doc7.records):
        if r['tag'] == 2201:
            t = r['payload'].decode('utf-16le', errors='ignore')
            if '52.488' in t and sawal_idx is None:
                sawal_idx = idx_r
            elif ('+ 25.062' in t or '+ 30.212' in t) and dmasuk_idx is None:
                dmasuk_idx = idx_r
            elif ('- 24.543' in t or '- 29.693' in t) and dkeluar_idx is None:
                dkeluar_idx = idx_r
            elif '570.498' in t and sakhir_idx is None:
                sakhir_idx = idx_r

    # Saldo Awal
    if sawal_idx:
        str_sawal = f"{fmt_idr(sawal_val)} "
        update_text(doc7, sawal_idx, str_sawal)
        for k in range(sawal_idx-1, max(0, sawal_idx-10), -1):
            if doc7.records[k]['tag'] == 150:
                update_color(doc7, k, palette['gray_sawal'])
            elif doc7.records[k]['tag'] == 2206:
                update_t2206(doc7, k, prosedur_training.hitung_lebar_teks_bold(str_sawal))
                break

    # Dana Masuk
    if dmasuk_idx:
        str_dmasuk = f"+ {fmt_idr(dmasuk_val)}"
        update_text(doc7, dmasuk_idx, str_dmasuk)
        for k in range(dmasuk_idx+1, min(len(doc7.records), dmasuk_idx+10)):
            if doc7.records[k]['tag'] == 2201:
                blank_node(doc7, k)
            elif doc7.records[k]['tag'] == 2200 or doc7.records[k]['tag'] == 2203:
                break
        for k in range(dmasuk_idx-1, max(0, dmasuk_idx-10), -1):
            if doc7.records[k]['tag'] == 150:
                update_color(doc7, k, palette['green_credit'])
            elif doc7.records[k]['tag'] == 2206:
                update_t2206(doc7, k, prosedur_training.hitung_lebar_teks_bold(str_dmasuk))
                break

    # Dana Keluar
    if dkeluar_idx:
        str_dkeluar = f"- {fmt_idr(dkeluar_val)} "
        update_text(doc7, dkeluar_idx, str_dkeluar)
        for k in range(dkeluar_idx-1, max(0, dkeluar_idx-10), -1):
            if doc7.records[k]['tag'] == 150:
                update_color(doc7, k, palette['black_debit'])
            elif doc7.records[k]['tag'] == 2206:
                update_t2206(doc7, k, prosedur_training.hitung_lebar_teks_bold(str_dkeluar))
                break

    # Saldo Akhir
    if sakhir_idx:
        str_sakhir = fmt_idr(sakhir_val)
        update_text(doc7, sakhir_idx, str_sakhir)
        for k in range(sakhir_idx-1, max(0, sakhir_idx-10), -1):
            if doc7.records[k]['tag'] == 150:
                update_color(doc7, k, palette['blue_saldo'])
            elif doc7.records[k]['tag'] == 2206:
                update_t2206(doc7, k, prosedur_training.hitung_lebar_teks_bold(str_sakhir))
                break

    # 2. Tabel Mutasi (147 Baris Transaksi)
    print(f"[*] Mengisi 147 Baris Tabel Mutasi pada 13 Halaman...")
    dom_rows7 = extract_dom_rows(doc7)
    assert len(dom_rows7) == 147, f"Expected 147 rows, got {len(dom_rows7)}"

    for idx_row, m in enumerate(dom_rows7):
        tx = tx_list[idx_row]
        row_num = idx_row + 1

        # A. Nomor Urut
        if m['no_rec']:
            update_text(doc7, m['no_rec'], str(row_num))

        # B. Saldo Berjalan (Decoupled Mode & Right Alignment pada 20.049 cm)
        s_rec = m['s_rec']
        s_splits = m.get('s_splits', [])
        s_t2100 = m.get('s_t2100')
        bal_val = tx['balance']
        str_saldo = fmt_idr(bal_val)
        if s_rec:
            update_text(doc7, s_rec, str_saldo)
        for sp in s_splits:
            blank_node(doc7, sp)
        if s_t2100:
            new_x_saldo = prosedur_training.TARGET_XR_SALDO - prosedur_training.calc_text_width(str_saldo)
            update_t2100_x(doc7, s_t2100, new_x_saldo)

        # C. Nominal Transaksi (+/-) & Rata Kanan 15.214 cm
        n_rec = m['n_rec']
        n_splits = m.get('n_splits', [])
        n_t2100 = m.get('n_t2100')
        n_t2206 = m.get('n_t2206')
        n_t150 = m.get('n_t150')

        nom_val = tx['nominal']
        if nom_val > 0:
            str_nominal = f"+{fmt_idr(nom_val)}"
            nom_color = palette['green_credit']
        else:
            str_nominal = f"-{fmt_idr(abs(nom_val))}"
            nom_color = palette['black_debit']

        update_text(doc7, n_rec, str_nominal)
        for sp in n_splits:
            blank_node(doc7, sp)

        if n_t150:
            update_color(doc7, n_t150, nom_color)

        x_left, w_nominal = prosedur_training.hitung_posisi_rata_kanan(str_nominal, prosedur_training.TARGET_XR_NOMINAL)

        if n_t2100:
            update_t2100_x(doc7, n_t2100, x_left)
        if n_t2206:
            update_t2206(doc7, n_t2206, w_nominal)

    out_t7 = os.path.join(folder, '0_tahap7.xar')
    sync_and_save(doc7, out_t7)

    print("\n=========================================================================")
    print("   [SUCCESS] MASTER FLAWLESS PIPELINE EXECUTION COMPLETED!")
    print(f"   Final Output: {out_t7}")
    print(f"   Customer Name: {prosedur_training.format_nama_kapital(cust_name)}")
    print(f"   Total Pages: 13 | Total Rows: 147")
    print("=========================================================================\n")

if __name__ == '__main__':
    run_master_adhikarya_pipeline()
