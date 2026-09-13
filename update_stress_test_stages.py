import json

history_file = 'training_history.json'
with open(history_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

t6_entry = {
    "stage": "Tahap 6 - Perubahan Tanggal Sesuai Periode & Jam",
    "input_file": r"C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar",
    "output_file": r"C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar",
    "period": "Dec 2026",
    "total_transaction_rows": 47,
    "primary_date_records_updated": 47,
    "trailing_digit_records_updated": 25,
    "total_records_updated_count": 72,
    "total_records_locked": 14392,
    "status": "PASS"
}

t7_entry = {
    "stage": "Tahap 7 - Perubahan Ringkasan & Tabel Transaksi Utama (FINAL)",
    "input_file": r"C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar",
    "output_file": r"C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7.xar",
    "summary_header": {
        "saldo_awal": "26.683,00",
        "dana_masuk": "+ 5.315.920,00",
        "dana_keluar": "- 4.210.600,00",
        "saldo_akhir": "1.132.003,00"
    },
    "total_transaction_rows_verified": 47,
    "modified_rows_count": 8,
    "modified_rows": [29, 30, 31, 32, 33, 34, 35, 36],
    "right_alignment_target": {
        "nominal_x_right_mp": 431320,
        "saldo_x_right_mp": 570450
    },
    "color_rules": {
        "credit_nominal": "Green (#00A651 / Tag 150)",
        "debit_nominal": "Black (#000000 / Tag 150)",
        "running_saldo": "Blue (#005B9C / Tag 150)"
    },
    "split_cleanup_rule": "Enforced b'\\x00\\x00' (2-byte null character) on Tag 2202 and Tag 2201 secondary nodes",
    "total_records_locked": 14392,
    "status": "PASS"
}

st2_stages = data["stress_test_2"]["stages"]
# Check if already added
stage_names = [s["stage"] for s in st2_stages]
if "Tahap 6 - Perubahan Tanggal Sesuai Periode & Jam" not in stage_names:
    st2_stages.append(t6_entry)
if "Tahap 7 - Perubahan Ringkasan & Tabel Transaksi Utama (FINAL)" not in stage_names:
    st2_stages.append(t7_entry)

with open(history_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print("Updated stress_test_2 stages in training_history.json successfully!")
