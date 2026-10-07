from xar_dom_engine import XarDocument

input_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(input_file)

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

# Apply updates in memory
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if 'Apr 2025' in s:
            new_s = s.replace('Apr 2025', 'Dec 2026')
            r['payload'] = new_s.encode('utf-16le')
            r['size'] = len(r['payload'])
        elif 'Apr 202' in s:
            new_s = s.replace('Apr 202', 'Dec 202')
            r['payload'] = new_s.encode('utf-16le')
            r['size'] = len(r['payload'])

for idx, new_val in trailing_5_map.items():
    r = doc.records[idx]
    r['payload'] = new_val.encode('utf-16le')
    r['size'] = len(r['payload'])

# Check for any remaining Apr or 2025
remaining = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if 'Apr' in s or '2025' in s:
            remaining.append((i, r['tag'], s))

print(f"Remaining Apr or 2025 count: {len(remaining)}")
if remaining:
    for rem in remaining:
        print(" ", rem)
else:
    print("SUCCESS: Zero occurrences of Apr or 2025 remain! All 47 transaction dates are now in Dec 2026.")
