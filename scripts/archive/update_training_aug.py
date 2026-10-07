import json

with open('training_history.json', 'r', encoding='utf-8') as f:
    history = json.load(f)

aug_entry = {
    "project": "PT_BENDI_NASHA_NIAGA_INDUSTRI_Marsiyah_Aug",
    "source_template_excel": "C:\\Users\\Lenovo\\Downloads\\rekening\\PT BENDI NASHA NIAGA INDUSTRI\\Marsiyah\\New folder\\aug\\Template_Pekerjaan_Xara_Aug.xlsx",
    "base_file": "C:\\Users\\Lenovo\\Downloads\\rekening\\PT BENDI NASHA NIAGA INDUSTRI\\Marsiyah\\New folder\\aug\\0.xar",
    "final_output": "C:\\Users\\Lenovo\\Downloads\\rekening\\PT BENDI NASHA NIAGA INDUSTRI\\Marsiyah\\New folder\\aug\\0_tahap7.xar",
    "customer_name": "MASRIYAH MUHAMMAD SAMIAN",
    "period": "01 Aug 2026 - 31 Aug 2026",
    "issued_date": "10 Sep 2026",
    "account_number": "1630016144514",
    "total_pages": 10,
    "total_records_locked": 28156,
    "total_transaction_rows": 110,
    "financial_summary": {
        "saldo_awal": "1.498.768,81",
        "dana_masuk": "+ 21.359.500,00",
        "dana_keluar": "- 21.685.780,00",
        "saldo_akhir": "1.172.488,81",
        "balance_status": "MATCH (1.498.768,81 + 21.359.500,00 - 21.685.780,00 = 1.172.488,81)"
    },
    "native_colors_profile": {
        "kredit_dana_masuk": "Tag 150 = b'\\xd3\\x03\\x00\\x00' (Native Document Green #00A651)",
        "debit_dana_keluar": "Tag 150 = b'\\x9e\\x01\\x00\\x00' (Native Document Black #000000)",
        "saldo_berjalan": "Tag 150 = b'\\x2b\\x05\\x00\\x00' (Native Document Blue #005B9C)",
        "saldo_awal": "Tag 150 = b'\\x6f\\x03\\x00\\x00' (Native Document Dark Gray #333333)"
    },
    "native_font_profile": {
        "font_id": 340,
        "tag_2907": "b'\\x54\\x01\\x00\\x00' (PDF-TTInterphases-Regular)",
        "tag_2906": "b'\\x40\\x1f\\x00\\x00' (Normal Style)",
        "anti_corruption_rule": "Zero foreign font IDs (55010000 prohibited) to ensure 0 pop-up warnings and preserve exact native font rendering"
    },
    "name_and_cabang_2box_standard": {
        "name_box": {
            "position": "X = 4.350 cm (123307 mp), Y = 25.964 cm (736000 mp)",
            "width": "W = 3.17 cm (Tag 2150 = 89858 mp, flag 1)",
            "line_spacing": "80% leading (Tag 4208/4209 = 400)",
            "font_size": "8pt (Tag 2901 = 10000 mp)",
            "font_id": "340 (Tag 2907 = 54010000)",
            "line_1": "MASRIYAH MUHAMMAD  (Tag 4211)",
            "line_2": "SAMIAN  (dy = -10000 mp, Tag 4211)",
            "trailing": "Tag 2206 (0, 0, -10000) and Tag 2203"
        },
        "cabang_box": {
            "object_type": "Independent single-line object (placed after Mandiri Call 14000 on each page)",
            "position": "X = 4.378 cm (124101 mp), Y = 25.203 cm (714420 mp)",
            "width": "0 (auto-fit)",
            "line_spacing": "80%",
            "font_size": "8pt (10000 mp)",
            "font_id": "340 (Tag 2907 = 54010000)",
            "text": "KCP Jakarta Taman Aries"
        }
    },
    "period_header_standard": {
        "text": "01 Aug 2026 - 31 Aug 2026",
        "phantom_space_clean": "Excised all orphan Tag 2202 blocks [1, 4405, 0, 2202, 1, 4405, 0] before Tag 4200 across all 10 pages for zero leading space",
        "container_width": "Tag 2150 = 180000 mp (6.35 cm)"
    },
    "stages_completed": [
        "Tahap 1: Perubahan Nama Nasabah pada 10 Halaman (0_tahap1.xar)",
        "Tahap 2: Perubahan Periode Laporan pada 10 Halaman (0_tahap2.xar)",
        "Tahap 3: Perubahan Tanggal Cetak pada 10 Halaman (0_tahap3.xar, 10 Sep 2026)",
        "Tahap 4: Perubahan Nomor Rekening pada Header Page 1 (0_tahap4.xar, 1630016144514)",
        "Tahap 5: Penomoran Halaman (0_tahap5.xar, 1 of 10 s.d. 10 of 10 / 1 dari 10 s.d. 10 dari 10)",
        "Tahap 6: Perubahan Tanggal (Aug 2026) & Jam Transaksi (0_tahap6.xar, 110 Baris + 18 secondary time nodes blanked)",
        "Tahap 7: Perubahan Ringkasan Header & Tabel Transaksi Utama (0_tahap7.xar, 110 Baris Nominal & Running Saldos right-aligned at X=15.217 cm)"
    ],
    "status": "PASS"
}

history["job_marsiyah_aug_2026"] = aug_entry

with open('training_history.json', 'w', encoding='utf-8') as f:
    json.dump(history, f, indent=2)

print("[*] Successfully updated training_history.json with job_marsiyah_aug_2026!")
