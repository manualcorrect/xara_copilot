import json

history_file = r'C:\Users\Lenovo\xara_copilot\training_history.json'
with open(history_file, 'r', encoding='utf-8') as f:
    history = json.load(f)

stress_test_3 = {
    'project': 'StressTest_3_Marsiyah_7Pages_73Rows',
    'base_template': r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar',
    'final_output': r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar',
    'total_pages': 7,
    'total_records_locked': 19597,
    'total_transaction_rows': 73,
    'customer_name': 'Masriyah Muhammad Samian',
    'account_number': '1630016144514',
    'period': '01 Jun 2026 - 30 Jun 2026',
    'dicetak_pada': '10 Sep 2026',
    'financial_summary': {
        'saldo_awal': '445.950,81',
        'dana_masuk': '+ 11.055.000,00',
        'dana_keluar': '- 5.123.603,00',
        'saldo_akhir': '6.377.347,81',
        'balance_status': 'MATCH'
    },
    'native_colors_profile': {
        'kredit_dana_masuk': "Tag 150 = b'\\xd6\\x03\\x00\\x00' (Native Green)",
        'debit_dana_keluar': "Tag 150 = b'\\x9d\\x01\\x00\\x00' (Native Black)",
        'saldo_berjalan': "Tag 150 = b'\\x28\\x05\\x00\\x00' (Native Blue)",
        'saldo_awal': "Tag 150 = b'\\x72\\x03\\x00\\x00' (Native Dark Gray)"
    },
    'stages_completed': [
        'Tahap 1: Perubahan Nama Nasabah pada 7 Halaman',
        'Tahap 2: Perubahan Periode Laporan pada 7 Halaman',
        'Tahap 3: Perubahan Tanggal Cetak pada 7 Halaman',
        'Tahap 4: Perubahan Nomor Rekening pada Header Page 1',
        'Tahap 5: Perubahan Nomor Halaman (1 of 7 s.d. 7 of 7)',
        'Tahap 6: Perubahan Tanggal (Jun 2026) & Jam Transaksi (Smart Scheduling 06:00 - 23:00 WIB) pada 73 Baris',
        'Tahap 7: Perubahan Ringkasan Header & Tabel Transaksi Utama (Deposit +6.355.000 Row 56 & Running Saldos)'
    ],
    'status': 'PASS'
}

history['stress_test_3'] = stress_test_3
with open(history_file, 'w', encoding='utf-8') as f:
    json.dump(history, f, indent=2)

print('[*] Successfully updated training_history.json with Stress Test 3 (7 Pages / 73 Rows)!')
