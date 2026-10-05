import sys
import json
import struct
from xar_dom_engine import XarDocument

sys.stdout.reconfigure(encoding='utf-8')

aug_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Aug"
xar_path = f"{aug_dir}\\0.xar"
doc = XarDocument(xar_path)

def get_txt(idx):
    if 0 <= idx < len(doc.records):
        r = doc.records[idx]
        if r['tag'] in (2201, 2202, 2203):
            return r['payload'].decode('utf-16le', errors='ignore')
    return ""

def get_pos(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2100:
        return struct.unpack('<iii', doc.records[idx]['payload'][:12])
    return None

def get_kern(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2206:
        return struct.unpack('<iii', doc.records[idx]['payload'][:12])
    return None

def get_color(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 150:
        return doc.records[idx]['payload'].hex()
    return None

# Let's inspect the neighborhoods of all 15 rows:
# Page 1:
# Row 1: Saldo Rec 1628, Nominal Rec 1649
# Row 2: Saldo Rec 1770, Nominal Rec 1791, 1796
# Row 3: Saldo Rec 1932, Nominal Rec 1953, 1958
# Row 4: Saldo Rec 2094, Nominal Rec 2115, 2120
# Row 5: Saldo Rec 2246, Nominal Rec 2267, 2272
# Row 6: Saldo Rec 2408, Nominal Rec 2429
# Row 7: Saldo Rec 2558, Nominal Rec 2579
# Row 8: Saldo Rec 2705, Nominal Rec 2726, 2731
# Row 9: Saldo Rec 2842, Nominal Rec 2863, 2868
# Row 10: Saldo Rec 3008, 3013, Nominal Rec 3034
# Page 2:
# Row 11: Saldo Rec 4196, Nominal Rec 4217, 4222
# Row 12: Saldo Rec 4353, Nominal Rec 4374
# Row 13: Saldo Rec 4490, Nominal Rec 4511
# Row 14: Saldo Rec 4637, Nominal Rec 4658
# Row 15: Saldo Rec 4799, 4804, Nominal Rec 4820

# Let's verify all tags for these 15 rows
row_candidates = [
    # (row, s_txt, s_split, n_txt, n_split, [d_recs], [t_recs])
    (1,  1628, None, 1649, None, [1694], [1669, 1674]),
    (2,  1770, None, 1791, 1796, [1841], [1816, 1821]),
    (3,  1932, None, 1953, 1958, [2003], [1978, 1983]),
    (4,  2094, None, 2115, 2120, [2170], [2140, 2145, 2150]),
    (5,  2246, None, 2267, 2272, [2297], [2277]), # let's check date/time for row 5
    (6,  2408, None, 2429, None, [2483], [2454]),
    (7,  2558, None, 2579, None, [2630], [2604]),
    (8,  2705, None, 2726, 2731, [2768], [2748]),
    (9,  2842, None, 2863, 2868, [2934], [2908]),
    (10, 3008, 3013, 3034, None, [3079], [3054]),
    (11, 4196, None, 4217, 4222, [4277], [4247]),
    (12, 4353, None, 4374, None, [4419], [4394]),
    (13, 4490, None, 4511, None, [4566], [4536]),
    (14, 4637, None, 4658, None, [4708], [4683]),
    (15, 4799, 4804, 4820, None, [4870], [4845])
]

# Let's write a script to inspect records in rows 5..15 precisely
for r_num in range(5, 16):
    print(f"\n--- Checking Row {r_num} text and tags ---")
    # Search around row
    # We will print all text nodes in that section
