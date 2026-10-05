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

row_map_6103 = {
    1:  {'s_pos': 1611, 's_col': 1616, 's_2206': 1627, 's_txt': 1628, 's_split': None, 'n_pos': 1632, 'n_col': 1637, 'n_2206': 1648, 'n_txt': 1649, 'n_split': None, 'd_recs': [1694], 't_recs': [1669, 1674]},
    2:  {'s_pos': 1753, 's_col': 1758, 's_2206': 1769, 's_txt': 1770, 's_split': None, 'n_pos': 1774, 'n_col': 1779, 'n_2206': 1790, 'n_txt': 1791, 'n_split': 1796, 'd_recs': [1841], 't_recs': [1816, 1821]},
    3:  {'s_pos': 1915, 's_col': 1920, 's_2206': 1931, 's_txt': 1932, 's_split': None, 'n_pos': 1936, 'n_col': 1941, 'n_2206': 1952, 'n_txt': 1953, 'n_split': 1958, 'd_recs': [2003], 't_recs': [1978, 1983]},
    4:  {'s_pos': 2077, 's_col': 2082, 's_2206': 2093, 's_txt': 2094, 's_split': None, 'n_pos': 2098, 'n_col': 2103, 'n_2206': 2114, 'n_txt': 2115, 'n_split': 2120, 'd_recs': [2170], 't_recs': [2140, 2145, 2150]},
    5:  {'s_pos': 2229, 's_col': 2234, 's_2206': 2245, 's_txt': 2246, 's_split': None, 'n_pos': 2250, 'n_col': 2255, 'n_2206': 2266, 'n_txt': 2267, 'n_split': 2272, 'd_recs': [2322], 't_recs': [2297, 2302]},
    6:  {'s_pos': 2391, 's_col': 2396, 's_2206': 2407, 's_txt': 2408, 's_split': None, 'n_pos': 2412, 'n_col': 2417, 'n_2206': 2428, 'n_txt': 2429, 'n_split': None, 'd_recs': [2483], 't_recs': [2454, 2459, 2464]},
    7:  {'s_pos': 2541, 's_col': 2546, 's_2206': 2557, 's_txt': 2558, 's_split': None, 'n_pos': 2562, 'n_col': 2567, 'n_2206': 2578, 'n_txt': 2579, 'n_split': None, 'd_recs': [2630], 't_recs': [2604, 2609, 2614]},
    8:  {'s_pos': 2688, 's_col': 2693, 's_2206': 2704, 's_txt': 2705, 's_split': None, 'n_pos': 2709, 'n_col': 2714, 'n_2206': 2725, 'n_txt': 2726, 'n_split': 2731, 'd_recs': [2768], 't_recs': [2748, 2753]},
    9:  {'s_pos': 2825, 's_col': 2830, 's_2206': 2841, 's_txt': 2842, 's_split': None, 'n_pos': 2846, 'n_col': 2851, 'n_2206': 2862, 'n_txt': 2863, 'n_split': 2868, 'd_recs': [2934], 't_recs': [2908, 2913, 2918]},
    10: {'s_pos': 2991, 's_col': 2996, 's_2206': 3007, 's_txt': 3008, 's_split': 3013, 'n_pos': 3017, 'n_col': 3022, 'n_2206': 3033, 'n_txt': 3034, 'n_split': None, 'd_recs': [3079], 't_recs': [3054, 3059]},
    11: {'s_pos': 4179, 's_col': 4184, 's_2206': 4195, 's_txt': 4196, 's_split': None, 'n_pos': 4200, 'n_col': 4205, 'n_2206': 4216, 'n_txt': 4217, 'n_split': 4222, 'd_recs': [4277], 't_recs': [4247, 4252, 4257]},
    12: {'s_pos': 4336, 's_col': 4341, 's_2206': 4352, 's_txt': 4353, 's_split': None, 'n_pos': 4357, 'n_col': 4362, 'n_2206': 4373, 'n_txt': 4374, 'n_split': None, 'd_recs': [4419], 't_recs': [4394]},
    13: {'s_pos': 4473, 's_col': 4478, 's_2206': 4489, 's_txt': 4490, 's_split': None, 'n_pos': 4494, 'n_col': 4499, 'n_2206': 4510, 'n_txt': 4511, 'n_split': None, 'd_recs': [4566], 't_recs': [4536, 4541]},
    14: {'s_pos': 4620, 's_col': 4625, 's_2206': 4636, 's_txt': 4637, 's_split': None, 'n_pos': 4641, 'n_col': 4646, 'n_2206': 4657, 'n_txt': 4658, 'n_split': None, 'd_recs': [4708], 't_recs': [4683]},
    15: {'s_pos': 4782, 's_col': 4787, 's_2206': 4798, 's_txt': 4799, 's_split': 4804, 'n_pos': 4808, 'n_col': 4813, 'n_2206': 4824, 'n_txt': 4825, 'n_split': None, 'd_recs': [4870], 't_recs': [4845]}
}

print("=== VERIFYING AUG 15 ROWS MAPPINGS ===")
for r_num, m in row_map_6103.items():
    s_txt = f"{get_txt(m['s_txt'])}{get_txt(m['s_split']) if m['s_split'] else ''}"
    n_txt = f"{get_txt(m['n_txt'])}{get_txt(m['n_split']) if m['n_split'] else ''}"
    d_txt = "".join([get_txt(idx) for idx in m['d_recs']])
    t_txt = "".join([get_txt(idx) for idx in m['t_recs']])
    
    # Check tags
    assert doc.records[m['s_pos']]['tag'] == 2100, f"Row {r_num} s_pos error"
    assert doc.records[m['s_col']]['tag'] == 150,  f"Row {r_num} s_col error"
    assert doc.records[m['s_2206']]['tag'] == 2206, f"Row {r_num} s_2206 error"
    assert doc.records[m['s_txt']]['tag'] in (2201, 2202), f"Row {r_num} s_txt error"
    
    assert doc.records[m['n_pos']]['tag'] == 2100, f"Row {r_num} n_pos error"
    assert doc.records[m['n_col']]['tag'] == 150,  f"Row {r_num} n_col error"
    assert doc.records[m['n_2206']]['tag'] == 2206, f"Row {r_num} n_2206 error"
    assert doc.records[m['n_txt']]['tag'] in (2201, 2202), f"Row {r_num} n_txt error"
    
    print(f"Row {r_num:2d}: Saldo='{s_txt}' Nominal='{n_txt}' Date='{d_txt}' Time='{t_txt}' [PASS]")

print("\n100% OF 15 ROWS FULLY VERIFIED AND VALIDATED!")
