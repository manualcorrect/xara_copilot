from xar_dom_engine import XarDocument
import re

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(target_file)

# Let's inspect each transaction row across all 5 pages
# We can find each row by looking around the 47 date records
date_records = [
    1761, 1939, 2102, 2244, 2414, 2581, 2743, 2880, 3052, 3189,
    4382, 4529, 4676, 4835, 4999, 5162, 5324, 5503, 5676, 5875, 6054, 6222,
    7377, 7555, 7707, 7880, 8056, 8206, 8386, 8556, 8724, 8861, 8973, 9110,
    10260, 10417, 10579, 10757, 10904, 11056, 11203, 11360, 11497, 11654, 11806, 11974,
    13169
]

print(f"Total transaction dates: {len(date_records)}")
for idx, d_rec in enumerate(date_records):
    # Find timestamp near d_rec
    time_str = "None"
    for j in range(max(0, d_rec-40), min(len(doc.records), d_rec+40)):
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            s = r['payload'].decode('utf-16le', errors='replace')
            if re.search(r'\b\d{1,2}:\d{2}', s):
                time_str = f"Rec {j}: {s}"
                break
    d_text = doc.records[d_rec]['payload'].decode('utf-16le', errors='replace')
    print(f"Row {idx+1:2d} | Date Rec {d_rec:5d}: {repr(d_text):15s} | Time: {time_str}")
