import json
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap5.xar')

# Exact row start records for all 73 rows:
row_starts = {
    1: 1568, 2: 1713, 3: 1853, 4: 2003, 5: 2158, 6: 2298, 7: 2448, 8: 2593, 9: 2733, 10: 2883,
    11: 3962, 12: 4128, 13: 4278, 14: 4418, 15: 4568, 16: 4713, 17: 4858, 18: 5013, 19: 5182, 20: 5332, 21: 5467, 22: 5627,
    23: 6716, 24: 6856, 25: 6996, 26: 7151, 27: 7308, 28: 7448, 29: 7588, 30: 7756, 31: 7919, 32: 8069, 33: 8219, 34: 8369,
    35: 9468, 36: 9618, 37: 9766, 38: 9921, 39: 10066, 40: 10224, 41: 10386, 42: 10531, 43: 10676, 44: 10831, 45: 10976, 46: 11124,
    47: 12240, 48: 12388, 49: 12538, 50: 12678, 51: 12833, 52: 12983, 53: 13123, 54: 13276, 55: 13426, 56: 13576, 57: 13716, 58: 13878,
    59: 14978, 60: 15123, 61: 15263, 62: 15431, 63: 15592, 64: 15747, 65: 15897, 66: 16037, 67: 16204, 68: 16363, 69: 16535, 70: 16690,
    71: 17858, 72: 18010, 73: 18150
}

sorted_rows = sorted(row_starts.keys())
row_date_time_map = {}

for idx, r_num in enumerate(sorted_rows):
    start = row_starts[r_num]
    end = row_starts[sorted_rows[idx+1]] if idx + 1 < len(sorted_rows) else 18350
    # Search all text records in [start, end)
    txts = []
    for i in range(start, min(start + 180, end)):
        r = doc.records[i]
        if r['tag'] in (2201, 2202):
            txt = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00').strip()
            if txt:
                txts.append((i, r['tag'], txt))

    # Identify date nodes
    d_nodes = []
    # Row 1 special: 1638 ('0'), 1642 ('1'), 1647 ('Jan 2026')
    if r_num == 1:
        d_nodes = [(1638, '0'), (1642, '1'), (1647, 'Jan 2026')]
    else:
        for t in txts:
            if any(m in t[2] for m in ['Jan 2026']) and 'WIB' not in t[2] and 'Periode' not in t[2] and 'Dicetak' not in t[2] and 'dari' not in t[2] and 'DANA' not in t[2]:
                d_nodes.append(t)
    
    # Identify time nodes
    t_nodes = []
    for t in txts:
        if 'WIB' in t[2] or (':' in t[2] and len(t[2]) >= 5 and any(c.isdigit() for c in t[2])):
            t_nodes.append(t)

    row_date_time_map[r_num] = {
        'date_nodes': [(d[0], d[1]) for d in d_nodes],
        'time_nodes': [(t[0], t[1]) for t in t_nodes]
    }

print("Sample Date & Time Nodes Map:")
for r in [1, 2, 4, 7, 8, 10, 11, 22, 57, 70, 73]:
    print(f"Row {r:2d}: D={row_date_time_map[r]['date_nodes']}, T={row_date_time_map[r]['time_nodes']}")

with open('row_date_time_map.json', 'w') as f:
    json.dump(row_date_time_map, f, indent=2)
print("Saved row_date_time_map.json")
