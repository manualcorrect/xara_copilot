import os
import sys
import json
import struct
from xar_dom_engine import XarDocument

def run_accurate_jul_pipeline():
    folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul'
    in_path = os.path.join(folder, '0.xar')

    print("=========================================================================")
    print("   PROJECT V2 PIPELINE (ACCURATE): MARSIYAH JULI 2026 (8 PAGES / 83 ROWS)")
    print(f"   Base Template: {in_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    TOTAL_RECS = len(doc.records)
    print(f"[*] Dokumen dimuat: {TOTAL_RECS:,} records")

    with open('jul_mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    with open('jul_final_tx_schedule.json', 'r', encoding='utf-8') as f:
        txs = json.load(f)

    with open('jul_detailed_rows.json', 'r', encoding='utf-8') as f:
        detailed_rows = json.load(f)

    # 1. Native Colors
    COLOR_GREEN = bytearray.fromhex('6f030000') # Native Green (Dana Masuk / Kredit)
    COLOR_BLACK = bytearray.fromhex('9e010000') # Native Black (Dana Keluar / Debit)
    COLOR_BLUE  = bytearray.fromhex('2b050000') # Native Blue (Saldo Akhir / Running Saldo)
    COLOR_GRAY  = bytearray.fromhex('6f030000') # Native Dark Gray (Saldo Awal)

    def update_text(d, rec_idx, text_str):
        p = bytearray(text_str.encode('utf-16le'))
        d.records[rec_idx]['payload'] = p
        d.records[rec_idx]['size'] = len(p)

    def blank_node(d, rec_idx):
        d.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        d.records[rec_idx]['size'] = 2

    def update_color(d, rec_idx, color_bytes):
        d.records[rec_idx]['payload'] = color_bytes
        d.records[rec_idx]['size'] = len(color_bytes)

    def update_t2206(d, rec_idx, new_w):
        orig = struct.unpack('<iii', d.records[rec_idx]['payload'][:12])
        d.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_w, orig[1], orig[2]))
        d.records[rec_idx]['size'] = 12

    def update_t2100(d, rec_idx, new_x, new_y):
        d.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, new_y, 1))
        d.records[rec_idx]['size'] = 12

    def update_t2204(d, rec_idx, new_dx, new_dy):
        d.records[rec_idx]['payload'] = bytearray(struct.pack('<ii', new_dx, new_dy))
        d.records[rec_idx]['size'] = 8

    def sync_and_save(d, out_path):
        for r in d.records:
            r['size'] = len(r['payload'])
        assert len(d.records) == TOTAL_RECS, f"Zero-shift violation! Expected {TOTAL_RECS}, got {len(d.records)}"
        zero_nodes = [i for i, r in enumerate(d.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
        assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"
        d.save(out_path)
        print(f"   [SAVED] {os.path.basename(out_path)} ({len(d.records):,} records) [PASS]")

    # =========================================================================
    # TAHAP 1: PERUBAHAN NAMA NASABAH (8 HALAMAN)
    # =========================================================================
    print("--- [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH ---")
    doc1 = XarDocument(in_path)
    NEW_NAME = "MASRIYAH MUHAMMAD SAMIAN "
    for item in mapping["customer_name"]:
        r_idx = item["rec_idx"]
        k_idx = item["kern_idx"]
        old_val = doc1.records[r_idx]['payload'].decode('utf-16le', errors='ignore')
        update_text(doc1, r_idx, NEW_NAME)
        if k_idx:
            w_old = struct.unpack('<iii', doc1.records[k_idx]['payload'][:12])[0]
            new_w = int(w_old * (len(NEW_NAME) / max(1, len(old_val))))
            update_t2206(doc1, k_idx, new_w)
    out_t1 = os.path.join(folder, '0_tahap1.xar')
    sync_and_save(doc1, out_t1)

    # =========================================================================
    # TAHAP 2: PERUBAHAN PERIODE LAPORAN (8 HALAMAN)
    # =========================================================================
    print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
    doc2 = XarDocument(out_t1)
    NEW_PERIOD = "01 Jul 2026 - 31 Jul 2026"
    for item in mapping["period"]:
        p_rec = item["rec_idx"]
        update_text(doc2, p_rec, NEW_PERIOD)
        sec_rec = p_rec + 5
        if doc2.records[sec_rec]['tag'] == 2202:
            blank_node(doc2, sec_rec)
    out_t2 = os.path.join(folder, '0_tahap2.xar')
    sync_and_save(doc2, out_t2)

    # =========================================================================
    # TAHAP 3: PERUBAHAN TANGGAL CETAK (8 HALAMAN)
    # =========================================================================
    print("\n--- [3/7] TAHAP 3: PERUBAHAN TANGGAL CETAK ---")
    doc3 = XarDocument(out_t2)
    for item in mapping["dicetak_pada"]:
        d_rec = item["rec_idx"]
        tens_rec = d_rec - 12
        units_rec = d_rec - 8
        update_text(doc3, tens_rec, "1")
        update_text(doc3, units_rec, "0")
        update_text(doc3, d_rec, "Sep 2026")
    out_t3 = os.path.join(folder, '0_tahap3.xar')
    sync_and_save(doc3, out_t3)

    # =========================================================================
    # TAHAP 4: PERUBAHAN NOMOR REKENING (HEADER PAGE 1)
    # =========================================================================
    print("\n--- [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING ---")
    doc4 = XarDocument(out_t3)
    acc_rec = mapping["account_number"]["rec_idx"]
    update_text(doc4, acc_rec, "1630016144514 ")
    out_t4 = os.path.join(folder, '0_tahap4.xar')
    sync_and_save(doc4, out_t4)

    # =========================================================================
    # TAHAP 5: PENOMORAN HALAMAN (8 HALAMAN)
    # =========================================================================
    print("\n--- [5/7] TAHAP 5: PENOMORAN HALAMAN ---")
    doc5 = XarDocument(out_t4)
    out_t5 = os.path.join(folder, '0_tahap5.xar')
    sync_and_save(doc5, out_t5)

    # =========================================================================
    # TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI (83 BARIS)
    # =========================================================================
    print("\n--- [6/7] TAHAP 6: TANGGAL & JAM TRANSAKSI (83 BARIS) ---")
    doc6 = XarDocument(out_t5)

    # Find all 83 date nodes
    date_recs = []
    for i, r in enumerate(doc6.records):
        if r['tag'] in (2201, 2202):
            t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
            if 'Feb 2026' in t and len(t) >= 10 and not any(w in t for w in ['-', 'Period', 'Periode']):
                date_recs.append(i)

    assert len(date_recs) == 83, f"Expected 83 date records, got {len(date_recs)}"

    for i in range(83):
        tx = txs[i]
        d_rec = date_recs[i]
        update_text(doc6, d_rec, tx["date_str"])
        
        # Find preceding time node before d_rec
        for tm in range(max(0, d_rec-35), d_rec):
            rtm = doc6.records[tm]
            if rtm['tag'] in (2201, 2202):
                t_str = rtm['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if 'WIB' in t_str or (':' in t_str and any(c.isdigit() for c in t_str)):
                    update_text(doc6, tm, tx["final_time"])
                    break

    out_t6 = os.path.join(folder, '0_tahap6.xar')
    sync_and_save(doc6, out_t6)

    # =========================================================================
    # TAHAP 7: PERUBAHAN RINGKASAN HEADER & TABEL TRANSAKSI (83 BARIS)
    # =========================================================================
    print("\n--- [7/7] TAHAP 7: RINGKASAN HEADER & TABEL TRANSAKSI (FINAL) ---")
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
    for i in range(83):
        tx = txs[i]
        d_row = detailed_rows[i]
        
        s_rec = d_row["saldo_rec"]
        k_rec = d_row["tag2204_rec"]
        nom_prim = d_row["nom_primary"]
        nom_sec = d_row["nom_secondary"]
        nom_col_rec = d_row["nom_tag150"]
        nom_t6 = d_row["nom_tag2206"]
        nom_t1 = d_row["nom_tag2100"]

        # Update Saldo Text & Tag 2204 Kern
        update_text(doc7, s_rec, tx["formatted_saldo"])
        update_t2204(doc7, k_rec, tx["calibrated_dx"], tx["calibrated_dy"])

        # Update Nominal Text & Blank Secondary Split
        if nom_prim:
            update_text(doc7, nom_prim, tx["formatted_nominal"])
            if nom_sec:
                blank_node(doc7, nom_sec)
                
            # Update Nominal Color Tag 150
            if nom_col_rec:
                if tx["nom_type"] == "CR":
                    update_color(doc7, nom_col_rec, COLOR_GREEN)
                else:
                    update_color(doc7, nom_col_rec, COLOR_BLACK)

    out_t7 = os.path.join(folder, '0_tahap7.xar')
    sync_and_save(doc7, out_t7)

    print("\n=========================================================================")
    print("   [SUCCESS] PIPELINE 7 TAHAP MARSIYAH JULI 2026 SELESAI 100%!")
    print(f"   Final Output File: {out_t7}")
    print("=========================================================================")

if __name__ == '__main__':
    run_accurate_jul_pipeline()
