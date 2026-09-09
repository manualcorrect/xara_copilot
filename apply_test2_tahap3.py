import sys
import os
import json
from xar_dom_engine import XarDocument

def apply_test2_tahap3():
    v2_in = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap2.xar'
    v2_out = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap3.xar'

    print("=========================================================================")
    print("   PROJECT V2 STRESS TEST (TEST 2): TAHAP 3 - PERUBAHAN TANGGAL CETAK")
    print("   Target: 5 Halaman Penuh (Multi-Page Scalability Test)")
    print(f"   Input File : {v2_in}")
    print(f"   Output File: {v2_out}")
    print("=========================================================================\n")

    doc = XarDocument(v2_in)
    print(f"[*] Loaded document successfully. Total records: {len(doc.records)}")

    # Target changes for '19 Jan 2027'
    # Day 2: '2' -> '9'
    # Month: 'Jul' -> 'Jan'
    # Year: ' 2026' -> ' 2027'
    b_day2 = bytearray('9'.encode('utf-16le'))
    b_month = bytearray('Jan'.encode('utf-16le'))
    b_year = bytearray(' 2027'.encode('utf-16le'))

    # Records across all 5 pages
    # Format: (page_num, day2_idx, month_idx, year_idx)
    target_pages = [
        (1, 1112, 1122, 1126),
        (2, 3903, 3913, 3917),
        (3, 6909, 6919, 6923),
        (4, 9852, 9862, 9866),
        (5, 12736, 12746, 12750)
    ]

    for page_num, d2_idx, m_idx, y_idx in target_pages:
        # Verify existing text
        old_d2 = doc.records[d2_idx]['payload'].decode('utf-16le')
        old_m = doc.records[m_idx]['payload'].decode('utf-16le')
        old_y = doc.records[y_idx]['payload'].decode('utf-16le')

        assert old_d2 == '2', f"Expected '2' at {d2_idx} on Page {page_num}, got {old_d2}"
        assert 'Jul' in old_m, f"Expected 'Jul' at {m_idx} on Page {page_num}, got {old_m}"
        assert '2026' in old_y, f"Expected '2026' at {y_idx} on Page {page_num}, got {old_y}"

        # Update payloads
        doc.records[d2_idx]['payload'] = b_day2
        doc.records[d2_idx]['size'] = len(b_day2)

        doc.records[m_idx]['payload'] = b_month
        doc.records[m_idx]['size'] = len(b_month)

        doc.records[y_idx]['payload'] = b_year
        doc.records[y_idx]['size'] = len(b_year)

        print(f"[*] Page {page_num}: Date updated from '1{old_d2} {old_m}{old_y}' -> '19 Jan 2027' (Recs {d2_idx}, {m_idx}, {y_idx})")

    # Auto-sync all record sizes
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save Tahap 3 output
    doc.save(v2_out)
    print(f"\n[SUCCESS] Tahap 3 executed cleanly! Saved output to:\n          {v2_out}")
    print(f"[*] Total records maintained: exactly {len(doc.records)} records (Zero pointer shift).")

    # Update training_history.json
    history_file = r'C:\Users\Lenovo\xara_copilot\training_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)

        if "stress_test_2" in history_data:
            t3_entry = {
                "stage": "Tahap 3 - Perubahan Tanggal Cetak",
                "input_file": v2_in,
                "output_file": v2_out,
                "new_dicetak_pada": "19 Jan 2027",
                "pages_updated": len(target_pages),
                "updated_records": [idx for _, d2, m, y in target_pages for idx in (d2, m, y)],
                "total_records_locked": len(doc.records),
                "status": "PASS"
            }
            history_data["stress_test_2"]["stages"] = [
                s for s in history_data["stress_test_2"]["stages"] if s["stage"] != t3_entry["stage"]
            ]
            history_data["stress_test_2"]["stages"].append(t3_entry)

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2)
            print("[*] Updated training_history.json with Stress Test 2 Tahap 3 record.")

if __name__ == '__main__':
    apply_test2_tahap3()
