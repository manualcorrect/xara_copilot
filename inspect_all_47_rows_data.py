from xar_dom_engine import XarDocument
import struct

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

date_records = [
    1761, 1939, 2102, 2244, 2414, 2581, 2743, 2880, 3052, 3189,
    4382, 4529, 4676, 4835, 4999, 5162, 5324, 5503, 5676, 5875, 6054, 6222,
    7377, 7555, 7707, 7880, 8056, 8206, 8386, 8556, 8724, 8861, 8973, 9110,
    10260, 10417, 10579, 10757, 10904, 11056, 11203, 11360, 11497, 11654, 11806, 11974,
    13169
]

# In each transaction block, let's identify all numeric records (Nominal & Saldo)
# Let's inspect the records between consecutive date records!
for row_idx in range(len(date_records)):
    start_rec = date_records[row_idx]
    end_rec = date_records[row_idx+1] if row_idx + 1 < len(date_records) else start_rec + 150
    # In some pages, start_rec to end_rec crosses page boundary, so let's cap at start_rec + 200
    if end_rec - start_rec > 250:
        end_rec = start_rec + 200
    
    # Collect all text records in this row
    row_texts = []
    for i in range(start_rec, end_rec):
        r = doc.records[i]
        if r['tag'] in (2201, 2202):
            s = r['payload'].decode('utf-16le', errors='replace')
            row_texts.append((i, r['tag'], s))
    
    # Filter for numbers with ',' or '.'
    num_texts = [t for t in row_texts if any(c in t[2] for c in [',00', '+', '-']) or (',' in t[2] and any(d.isdigit() for d in t[2]))]
    print(f"Row {row_idx+1:2d} (starts at {start_rec}): {num_texts}")
