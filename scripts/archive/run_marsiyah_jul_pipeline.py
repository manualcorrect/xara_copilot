import os
import sys
import json
import struct
from xar_dom_engine import XarDocument

def run_pipeline():
    folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul'
    in_path = os.path.join(folder, '0.xar')

    print("=========================================================================")
    print("   PROJECT V2 PIPELINE EXECUTION: MARSIYAH JULI 2026 (8 PAGES / 83 ROWS)")
    print(f"   Base File: {in_path}")
    print("=========================================================================\n")

    with open('jul_mapping.json', 'r', encoding='utf-8') as f:
        mapping = json.load(f)

    with open('jul_final_tx_schedule.json', 'r', encoding='utf-8') as f:
        txs = json.load(f)

    # Native Colors in jul 0.xar
    COLOR_GREEN = bytearray.fromhex('6f030000') # Native Green (Dana Masuk / Kredit)
    COLOR_BLACK = bytearray.fromhex('9e010000') # Native Black (Dana Keluar / Debit)
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

    def update_t2100(doc, rec_idx, new_x, new_y):
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, new_y, 1))
        doc.records[rec_idx]['size'] = 12

    def update_t2204(doc, rec_idx, new_dx, new_dy):
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<ii', new_dx, new_dy))
        doc.records[rec_idx]['size'] = 8

    def sync_and_save(doc, out_path, expected_recs):
        for r in doc.records:
            r['size'] = len(r['payload'])
        assert len(doc.records) == expected_recs, f"Zero-shift violation! Expected {expected_recs}, got {len(doc.records)}"
        zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
        assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"
        doc.save(out_path)
        print(f"   [SAVED] {os.path.basename(out_path)} ({len(doc.records):,} records) [PASS]")

    # =========================================================================
    # TAHAP 1: PERUBAHAN NAMA NASABAH (8 HALAMAN)
    # =========================================================================
    print("--- [1/7] TAHAP 1: PERUBAHAN NAMA NASABAH ---")
    doc1 = XarDocument(in_path)
    TOTAL_RECS = len(doc1.records)
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
    sync_and_save(doc1, out_t1, TOTAL_RECS)

    # =========================================================================
    # TAHAP 2: PERUBAHAN PERIODE LAPORAN (8 HALAMAN)
    # =========================================================================
    print("\n--- [2/7] TAHAP 2: PERUBAHAN PERIODE LAPORAN ---")
    doc2 = XarDocument(out_t1)
    NEW_PERIOD = "01 Jul 2026 - 31 Jul 2026"
    for item in mapping["period"]:
        p_rec = item["rec_idx"]
        update_text(doc2, p_rec, NEW_PERIOD)
        # Blank secondary digit node (p_rec + 5)
        sec_rec = p_rec + 5
        if doc2.records[sec_rec]['tag'] == 2202:
            blank_node(doc2, sec_rec)
    out_t2 = os.path.join(folder, '0_tahap2.xar')
    sync_and_save(doc2, out_t2, TOTAL_RECS)

    # =========================================================================
    # TAHAP 3: PERUBAHAN TANGGAL CETAK (8 HALAMAN)
    # =========================================================================
    print("\n--- [3/7] TAHAP 3: PERUBAHAN TANGGAL CETAK ---")
    doc3 = XarDocument(out_t2)
    # Update '09 Sep 2026' -> '10 Sep 2026'
    for item in mapping["dicetak_pada"]:
        d_rec = item["rec_idx"]
        tens_rec = d_rec - 12
        units_rec = d_rec - 8
        update_text(doc3, tens_rec, "1")
        update_text(doc3, units_rec, "0")
        update_text(doc3, d_rec, "Sep 2026")
    out_t3 = os.path.join(folder, '0_tahap3.xar')
    sync_and_save(doc3, out_t3, TOTAL_RECS)

    # =========================================================================
    # TAHAP 4: PERUBAHAN NOMOR REKENING (HEADER PAGE 1)
    # =========================================================================
    print("\n--- [4/7] TAHAP 4: PERUBAHAN NOMOR REKENING ---")
    doc4 = XarDocument(out_t3)
    acc_rec = mapping["account_number"]["rec_idx"]
    NEW_ACC = "1630016144514 "
    update_text(doc4, acc_rec, NEW_ACC)
    out_t4 = os.path.join(folder, '0_tahap4.xar')
    sync_and_save(doc4, out_t4, TOTAL_RECS)

    # =========================================================================
    # TAHAP 5: VERIFIKASI & PENGUNCIAN PENOMORAN HALAMAN
    # =========================================================================
    print("\n--- [5/7] TAHAP 5: PENOMORAN HALAMAN ---")
    doc5 = XarDocument(out_t4)
    # All 8 pages are already '1 of 8' .. '8 of 8' and '1 dari 8' .. '8 dari 8'
    out_t5 = os.path.join(folder, '0_tahap5.xar')
    sync_and_save(doc5, out_t5, TOTAL_RECS)

    # =========================================================================
    # TAHAP 6: PERUBAHAN TANGGAL & JAM TRANSAKSI (83 BARIS)
    # =========================================================================
    print("\n--- [6/7] TAHAP 6: TANGGAL & JAM TRANSAKSI (83 BARIS) ---")
    doc6 = XarDocument(out_t5)
    for tx in txs:
        d_rec = tx["xar_row_info"]["date_rec"]
        t_rec = tx["xar_row_info"]["time_rec"]
        new_d = tx["date_str"]
        new_t = tx["final_time"]
        if d_rec:
            update_text(doc6, d_rec, new_d)
        if t_rec:
            update_text(doc6, t_rec, new_t)
    out_t6 = os.path.join(folder, '0_tahap6.xar')
    sync_and_save(doc6, out_t6, TOTAL_RECS)

    # =========================================================================
    # TAHAP 7: PERUBAHAN RINGKASAN HEADER & TABEL TRANSAKSI (83 BARIS)
    # =========================================================================
    print("\n--- [7/7] TAHAP 7: RINGKASAN HEADER & TABEL TRANSAKSI ---")
    doc7 = XarDocument(out_t6)

    # 1. Update Financial Summary Header
    # Saldo Awal: Rec 1175 ('21.347,81 ')
    update_text(doc7, 1175, "21.347,81 ")
    update_color(doc7, 1171, COLOR_GRAY)

    # Dana Masuk: Rec 1184 ('+ 13.811.000,00'), Rec 1189 (blank)
    update_text(doc7, 1184, "+ 13.811.000,00")
    blank_node(doc7, 1189)
    update_color(doc7, 1180, COLOR_GREEN)
    update_t2206(doc7, 1179, 65000)

    # Dana Keluar: Rec 1202 ('- 12.333.579,00 ')
    update_text(doc7, 1202, "- 12.333.579,00 ")
    update_color(doc7, 1195, COLOR_BLACK)
    update_t2206(doc7, 1194, 68000)

    # Saldo Akhir: Rec 1215 ('1.498.768,81')
    update_text(doc7, 1215, "1.498.768,81")
    update_color(doc7, 1208, COLOR_BLUE)
    update_t2206(doc7, 1206, 43894)

    print("   [*] Financial Summary Header updated: Saldo Awal='21.347,81', Masuk='+ 13.811.000,00', Keluar='- 12.333.579,00', Akhir='1.498.768,81'")

    # 2. Update all 83 transaction rows
    for tx in txs:
        r_info = tx["xar_row_info"]
        s_rec = r_info["saldo_rec"]
        k_rec = r_info["tag2204_rec"]
        nom_rec = r_info["nominal_rec"]
        t6_rec = r_info["nom_tag2206"]
        t1_rec = r_info["nom_tag2100"]

        # Update Saldo Text & Tag 2204 Kern
        update_text(doc7, s_rec, tx["formatted_saldo"])
        update_t2204(doc7, k_rec, tx["calibrated_dx"], tx["calibrated_dy"])

        # Update Nominal Text & Color
        if nom_rec:
            update_text(doc7, nom_rec, tx["formatted_nominal"])
            # Color Tag 150
            if tx["nom_type"] == "CR":
                # Find tag 150 before nom_rec
                for c in range(max(0, nom_rec-20), nom_rec):
                    if doc7.records[c]['tag'] == 150:
                        update_color(doc7, c, COLOR_GREEN)
                        break
            else:
                for c in range(max(0, nom_rec-20), nom_rec):
                    if doc7.records[c]['tag'] == 150:
                        update_color(doc7, c, COLOR_BLACK)
                        break

    out_t7 = os.path.join(folder, '0_tahap7.xar')
    sync_and_save(doc7, out_t7, TOTAL_RECS)

    print("\n=========================================================================")
    print(f"   [SUCCESS] PIPELINE 7 TAHAP MARSIYAH JULI 2026 SELESAI 100%!")
    print(f"   Final Output: {out_t7}")
    print("=========================================================================")

if __name__ == '__main__':
    run_pipeline()
