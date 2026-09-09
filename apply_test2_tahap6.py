import json
import os
from xar_dom_engine import XarDocument

input_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
output_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'

print("=" * 60)
print("PROJECT V2 - TEST 2 (STRESS TEST): TAHAP 6 EXECUTION")
print("Target: Perubahan Tanggal Sesuai Periode (Dec 2026) Seluruh Baris Transaksi")
print("=" * 60)

doc = XarDocument(input_file)
initial_count = len(doc.records)
print(f"Loaded {initial_count} records from: {input_file}")

# Trailing year-digit records mapping for split date nodes
trailing_5_map = {
    4387: '6',
    4534: '6',
    4681: '6',
    4840: '6',
    5004: '6',
    5167: '6',
    5329: '6',
    5508: '6',
    5681: '6',
    7885: '6',
    8395: '6 ',
    8561: '6',
    8729: '6',
    8866: '6',
    8978: '6',
    9115: '6',
    10265: '6',
    10422: '6',
    10584: '6',
    10762: '6',
    10909: '6',
    11061: '6',
    11208: '6',
    11365: '6',
    11502: '6'
}

primary_updates = []
# 1. Update primary date records
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if 'Apr 2025' in s:
            new_s = s.replace('Apr 2025', 'Dec 2026')
            r['payload'] = new_s.encode('utf-16le')
            r['size'] = len(r['payload'])
            primary_updates.append((i, r['tag'], s, new_s))
        elif 'Apr 202' in s:
            new_s = s.replace('Apr 202', 'Dec 202')
            r['payload'] = new_s.encode('utf-16le')
            r['size'] = len(r['payload'])
            primary_updates.append((i, r['tag'], s, new_s))

# 2. Update trailing year-digit records
trailing_updates = []
for idx, new_val in trailing_5_map.items():
    r = doc.records[idx]
    old_val = r['payload'].decode('utf-16le', errors='replace')
    r['payload'] = new_val.encode('utf-16le')
    r['size'] = len(r['payload'])
    trailing_updates.append((idx, r['tag'], old_val, new_val))

total_modified = len(primary_updates) + len(trailing_updates)
print(f"Primary date records updated: {len(primary_updates)}")
print(f"Trailing digit records updated: {len(trailing_updates)}")
print(f"Total modified records: {total_modified}")

# Save output
doc.save(output_file)
print(f"Successfully saved to: {output_file}")

# Verification
print("\n--- RUNNING POST-SAVE VERIFICATION ---")
doc_verify = XarDocument(output_file)
verify_count = len(doc_verify.records)
print(f"Verified Record Count: {verify_count} (Expected: {initial_count})")
assert verify_count == initial_count, f"Record count changed! {verify_count} != {initial_count}"

# Check for size mismatches
size_mismatches = 0
for i, r in enumerate(doc_verify.records):
    if len(r['payload']) != r['size']:
        size_mismatches += 1
print(f"Size Mismatches: {size_mismatches} (Expected: 0)")
assert size_mismatches == 0, f"Found {size_mismatches} size mismatches!"

# Check for any remaining Apr or 2025
remaining_old = []
for i, r in enumerate(doc_verify.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if 'Apr' in s or '2025' in s:
            remaining_old.append((i, r['tag'], s))

print(f"Remaining 'Apr' or '2025' records: {len(remaining_old)} (Expected: 0)")
assert len(remaining_old) == 0, f"Found remaining old dates: {remaining_old}"

# Count total Dec 2026 occurrences
dec_2026_count = 0
for i, r in enumerate(doc_verify.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if 'Dec 2026' in s or 'Dec 202' in s:
            dec_2026_count += 1
print(f"Total 'Dec 2026' / 'Dec 202' records in file: {dec_2026_count}")

print("\nTAHAP 6 EXECUTION AND VERIFICATION: 100% SUCCESS!")

# Update training history
history_file = 'training_history.json'
if os.path.exists(history_file):
    with open(history_file, 'r', encoding='utf-8') as f:
        history = json.load(f)
else:
    history = {}

tahap6_entry = {
    "stage": "Tahap 6 - Perubahan Tanggal Sesuai Periode & Jam (Stress Test 2)",
    "input_file": input_file,
    "output_file": output_file,
    "period": "Dec 2026",
    "total_transaction_rows": 47,
    "primary_date_records_updated": len(primary_updates),
    "trailing_digit_records_updated": len(trailing_updates),
    "total_records_updated_count": total_modified,
    "total_records_locked": verify_count,
    "status": "PASS"
}

if "training_stages" not in history:
    history["training_stages"] = []
history["training_stages"].append(tahap6_entry)

with open(history_file, 'w', encoding='utf-8') as f:
    json.dump(history, f, indent=2)
print("Updated training_history.json successfully.")
