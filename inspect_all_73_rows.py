import json
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap5.xar')

# Known row number records:
row_no_records = {
    1: 1568, 2: 1713, 3: 1853, 4: 2003, 5: 2158, 6: 2298, 7: 2448, 8: 2593, 9: 2733, 10: 2883,
    11: 3962, 12: 4128, 13: 4278, 14: 4418, 15: 4568, 16: 4713, 17: 4858, 18: 5013, 19: 5182, 20: 5332, 21: 5467, 22: 5627,
    23: 6716, 24: 6856, 25: 6996, 26: 7151, 27: 7308, 28: 7448, 29: 7588, 30: 7756, 31: 7919, 32: 8069, 33: 8219, 34: 8369,
    35: 9468, 36: 9618, 37: 9766, 38: 9921, 39: 10066, 40: 10224, 41: 10386, 42: 10531, 43: 10676, 44: 10831, 45: 10976, 46: 11124,
    47: 12240, 48: 12388, 49: 12538, 50: 12678, 51: 12833, 52: 12983, 53: 13123, 54: 13276, 55: 13426, 56: 13576, 57: (13716, 13728), 58: 13878,
    59: 14978, 60: 15123, 61: 15263, 62: 15431, 63: 15592, 64: 15747, 65: 15897, 66: 16037, 67: 16204, 68: 16363, 69: 16535, 70: (16690, 16702),
    71: 17858, 72: 18010, 73: 18150
}

# Next boundary after each row
next_bounds = []
sorted_rows = sorted(row_no_records.keys())
for idx, r_num in enumerate(sorted_rows):
    curr_rec = row_no_records[r_num]
    start_rec = curr_rec if isinstance(curr_rec, int) else curr_rec[0]
    if idx + 1 < len(sorted_rows):
        nxt_rec = row_no_records[sorted_rows[idx + 1]]
        end_rec = nxt_rec if isinstance(nxt_rec, int) else nxt_rec[0]
    else:
        end_rec = 18350
    next_bounds.append((r_num, start_rec, end_rec))

row_map = {}

for r_num, start_rec, end_rec in next_bounds:
    # Look at all text records between start_rec and end_rec
    info = {'no': r_num, 'start': start_rec, 'end': end_rec, 'texts': []}
    for i in range(start_rec, end_rec):
        r = doc.records[i]
        if r['tag'] in (2201, 2202):
            txt = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00').strip()
            if txt:
                info['texts'].append((i, r['tag'], txt))
    row_map[r_num] = info

print(f"Mapped {len(row_map)} rows.")
# Print sample rows: Row 1, Row 11, Row 23, Row 35, Row 47, Row 57, Row 70, Row 73
for r_num in [1, 11, 23, 35, 47, 57, 70, 73]:
    print(f"\n--- ROW {r_num} (Rec {row_map[r_num]['start']}..{row_map[r_num]['end']}) ---")
    for t in row_map[r_num]['texts']:
        print(f"  Rec {t[0]:5d}: Tag {t[1]} -> {repr(t[2])}")
