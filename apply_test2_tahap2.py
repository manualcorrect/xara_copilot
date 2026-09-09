import sys
import os
import json
from xar_dom_engine import XarDocument

def apply_test2_tahap2():
    v2_in = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap1.xar'
    v2_out = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap2.xar'

    print("=========================================================================")
    print("   PROJECT V2 STRESS TEST (TEST 2): TAHAP 2 - PERUBAHAN PERIODE LAPORAN")
    print("   Target: 5 Halaman Penuh (Multi-Page Scalability Test)")
    print(f"   Input File : {v2_in}")
    print(f"   Output File: {v2_out}")
    print("=========================================================================\n")

    doc = XarDocument(v2_in)
    print(f"[*] Loaded document successfully. Total records: {len(doc.records)}")

    # Target strings to replace
    NEW_PART_1 = "Dec 2026 - "
    NEW_PART_2 = "1 Dec 2026"

    p1_bytes = bytearray(NEW_PART_1.encode('utf-16le'))
    p2_bytes = bytearray(NEW_PART_2.encode('utf-16le'))

    # Record pairs across all 5 pages
    # Format: (page_num, part1_idx, part2_idx)
    target_pages = [
        (1, 1078, 1084),
        (2, 3878, 3884),
        (3, 6884, 6890),
        (4, 9827, 9833),
        (5, 12711, 12717)
    ]

    for page_num, idx1, idx2 in target_pages:
        # Verify existing text
        old_p1 = doc.records[idx1]['payload'].decode('utf-16le', errors='replace')
        old_p2 = doc.records[idx2]['payload'].decode('utf-16le', errors='replace')
        assert 'Apr 2025' in old_p1, f"Expected Apr 2025 at {idx1} Page {page_num}, got {old_p1}"
        assert 'Apr 2025' in old_p2, f"Expected Apr 2025 at {idx2} Page {page_num}, got {old_p2}"

        # Update Part 1 (Apr 2025 - -> Dec 2026 - )
        doc.records[idx1]['payload'] = p1_bytes
        doc.records[idx1]['size'] = len(p1_bytes)

        # Update Part 2 (0 Apr 2025 -> 1 Dec 2026)
        doc.records[idx2]['payload'] = p2_bytes
        doc.records[idx2]['size'] = len(p2_bytes)

        print(f"[*] Page {page_num}: Rec {idx1:05d} ('{old_p1}' -> '{NEW_PART_1}'), Rec {idx2:05d} ('{old_p2}' -> '{NEW_PART_2}')")

    # Auto-sync all record sizes
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save Tahap 2 output
    doc.save(v2_out)
    print(f"\n[SUCCESS] Tahap 2 executed cleanly! Saved output to:\n          {v2_out}")
    print(f"[*] Total records maintained: exactly {len(doc.records)} records (Zero pointer shift).")

    # Update training_history.json
    history_file = r'C:\Users\Lenovo\xara_copilot\training_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)

        if "stress_test_2" in history_data:
            t2_entry = {
                "stage": "Tahap 2 - Perubahan Periode",
                "input_file": v2_in,
                "output_file": v2_out,
                "new_period": "01 Dec 2026 - 31 Dec 2026",
                "pages_updated": len(target_pages),
                "updated_records": [idx for _, i1, i2 in target_pages for idx in (i1, i2)],
                "total_records_locked": len(doc.records),
                "status": "PASS"
            }
            history_data["stress_test_2"]["stages"] = [
                s for s in history_data["stress_test_2"]["stages"] if s["stage"] != t2_entry["stage"]
            ]
            history_data["stress_test_2"]["stages"].append(t2_entry)

            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, indent=2)
            print("[*] Updated training_history.json with Stress Test 2 Tahap 2 record.")

if __name__ == '__main__':
    apply_test2_tahap2()
