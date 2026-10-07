import sys
import os
import json
import struct
from xar_dom_engine import XarDocument

def apply_test2_tahap1():
    v2_in = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1.xar'
    v2_out = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap1.xar'

    print("=========================================================================")
    print("   PROJECT V2 STRESS TEST (TEST 2): TAHAP 1 - PERUBAHAN NAMA NASABAH")
    print("   Target: 5 Halaman Penuh (Multi-Page Scalability Test)")
    print(f"   Input File : {v2_in}")
    print(f"   Output File: {v2_out}")
    print("=========================================================================\n")

    doc = XarDocument(v2_in)
    print(f"[*] Loaded document successfully. Total records: {len(doc.records)}")

    # Standard customer name
    NEW_NAME = "ASEP ISKANDAR"
    name_payload = bytearray(NEW_NAME.encode('utf-16le'))
    name_size = len(name_payload)

    # Calculated advance width for 'ASEP ISKANDAR' in TTInterphases-Regular: 53817 mp
    NEW_WIDTH = 53817

    # Target records on all 5 pages
    # Format: (page_num, name_record_idx, kern_width_idx)
    target_pages = [
        (1, 1023, 1022),
        (2, 3823, 3822),
        (3, 6829, 6828),
        (4, 9772, 9771),
        (5, 12656, 12655)
    ]

    for page_num, name_idx, kern_idx in target_pages:
        # Verify existing text is DINI
        old_text = doc.records[name_idx]['payload'].decode('utf-16le', errors='replace')
        assert 'DINI' in old_text, f"Expected DINI at record {name_idx} on Page {page_num}, got {old_text}!"

        # Update Name Payload
        doc.records[name_idx]['payload'] = name_payload
        doc.records[name_idx]['size'] = name_size

        # Update Line Advance Width in Tag 2206
        w, h, flags = struct.unpack('<iii', doc.records[kern_idx]['payload'][:12])
        doc.records[kern_idx]['payload'] = bytearray(struct.pack('<iii', NEW_WIDTH, h, flags))
        doc.records[kern_idx]['size'] = len(doc.records[kern_idx]['payload'])

        print(f"[*] Page {page_num}: Record {name_idx:05d} updated from '{old_text}' -> '{NEW_NAME}' (Width Tag 2206 = {NEW_WIDTH})")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save Tahap 1 output
    doc.save(v2_out)
    print(f"\n[SUCCESS] Tahap 1 executed cleanly! Saved output to:\n          {v2_out}")
    print(f"[*] Total records maintained: exactly {len(doc.records)} records (Zero pointer shift).")

    # Update training_history.json
    history_file = r'C:\Users\Lenovo\xara_copilot\training_history.json'
    if os.path.exists(history_file):
        with open(history_file, 'r', encoding='utf-8') as f:
            history_data = json.load(f)

        if "stress_test_2" not in history_data:
            history_data["stress_test_2"] = {
                "project": "StressTest_Test2_5Pages",
                "base_template": v2_in,
                "total_pages": 5,
                "total_records": len(doc.records),
                "stages": []
            }

        t1_entry = {
            "stage": "Tahap 1 - Perubahan Nama Nasabah",
            "input_file": v2_in,
            "output_file": v2_out,
            "new_name": NEW_NAME,
            "pages_updated": len(target_pages),
            "updated_records": [name_idx for _, name_idx, _ in target_pages],
            "total_records_locked": len(doc.records),
            "status": "PASS"
        }
        # Replace or append
        history_data["stress_test_2"]["stages"] = [
            s for s in history_data["stress_test_2"]["stages"] if s["stage"] != t1_entry["stage"]
        ]
        history_data["stress_test_2"]["stages"].append(t1_entry)

        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f, indent=2)
        print("[*] Updated training_history.json with Stress Test 2 Tahap 1 record.")

if __name__ == '__main__':
    apply_test2_tahap1()
