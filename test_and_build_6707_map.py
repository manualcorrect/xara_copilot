import sys
import json
import struct
from xar_dom_engine import XarDocument

sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

# Let's verify every row mapping
row_map_6707 = {
    1:  {'s_pos': 1571, 's_col': 1576, 's_2206': 1587, 's_txt': 1588, 's_split': None, 'n_pos': 1592, 'n_col': 1597, 'n_2206': 1608, 'n_txt': 1609, 'n_split': 1614, 'd_recs': [1654], 't_recs': [1634]},
    2:  {'s_pos': 1728, 's_col': 1733, 's_2206': 1744, 's_txt': 1745, 's_split': None, 'n_pos': 1749, 'n_col': 1754, 'n_2206': 1765, 'n_txt': 1766, 'n_split': 1771, 'd_recs': [1816], 't_recs': [1791, 1796]},
    3:  {'s_pos': 1895, 's_col': 1900, 's_2206': 1911, 's_txt': 1912, 's_split': None, 'n_pos': 1916, 'n_col': 1921, 'n_2206': 1932, 'n_txt': 1933, 'n_split': None, 'd_recs': [1978], 't_recs': [1953, 1958]},
    4:  {'s_pos': 2067, 's_col': 2072, 's_2206': 2083, 's_txt': 2084, 's_split': None, 'n_pos': 2088, 'n_col': 2093, 'n_2206': 2104, 'n_txt': 2105, 'n_split': 2110, 'd_recs': [2155], 't_recs': [2130, 2135]},
    5:  {'s_pos': 2244, 's_col': 2249, 's_2206': 2260, 's_txt': 2261, 's_split': None, 'n_pos': 2265, 'n_col': 2270, 'n_2206': 2281, 'n_txt': 2282, 'n_split': 2287, 'd_recs': [2332], 't_recs': [2307, 2312]},
    6:  {'s_pos': 2386, 's_col': 2391, 's_2206': 2402, 's_txt': 2403, 's_split': None, 'n_pos': 2407, 'n_col': 2412, 'n_2206': 2423, 'n_txt': 2424, 'n_split': None, 'd_recs': [2469], 't_recs': [2444, 2449]},
    7:  {'s_pos': 2543, 's_col': 2548, 's_2206': 2559, 's_txt': 2560, 's_split': None, 'n_pos': 2564, 'n_col': 2569, 'n_2206': 2580, 'n_txt': 2581, 'n_split': 2586, 'd_recs': [2631], 't_recs': [2606, 2611]},
    8:  {'s_pos': 2715, 's_col': 2720, 's_2206': 2731, 's_txt': 2732, 's_split': None, 'n_pos': 2736, 'n_col': 2741, 'n_2206': 2752, 'n_txt': 2753, 'n_split': 2758, 'd_recs': [2803], 't_recs': [2778, 2783]},
    9:  {'s_pos': 2896, 's_col': 2901, 's_2206': 2912, 's_txt': 2913, 's_split': None, 'n_pos': 2917, 'n_col': 2922, 'n_2206': 2933, 'n_txt': 2934, 'n_split': None, 'd_recs': [2979], 't_recs': [2954, 2959]},
    10: {'s_pos': 3033, 's_col': 3038, 's_2206': 3049, 's_txt': 3050, 's_split': None, 'n_pos': 3054, 'n_col': 3059, 'n_2206': 3070, 'n_txt': 3071, 'n_split': 3076, 'd_recs': [3121], 't_recs': [3096, 3101]},
    11: {'s_pos': 4142, 's_col': 4147, 's_2206': 4158, 's_txt': 4159, 's_split': None, 'n_pos': 4163, 'n_col': 4168, 'n_2206': 4179, 'n_txt': 4180, 'n_split': 4185, 'd_recs': [4225], 't_recs': [4205]},
    12: {'s_pos': 4286, 's_col': 4291, 's_2206': 4302, 's_txt': 4303, 's_split': None, 'n_pos': 4307, 'n_col': 4312, 'n_2206': 4323, 'n_txt': 4324, 'n_split': 4329, 'd_recs': [4374], 't_recs': [4349, 4354]},
    13: {'s_pos': 4428, 's_col': 4433, 's_2206': 4444, 's_txt': 4445, 's_split': None, 'n_pos': 4449, 'n_col': 4454, 'n_2206': 4465, 'n_txt': 4466, 'n_split': 4471, 'd_recs': [4516], 't_recs': [4491, 4496]},
    14: {'s_pos': 4570, 's_col': 4575, 's_2206': 4586, 's_txt': 4587, 's_split': None, 'n_pos': 4591, 'n_col': 4596, 'n_2206': 4607, 'n_txt': 4608, 'n_split': 4613, 'd_recs': [4658], 't_recs': [4633, 4638]},
    15: {'s_pos': 4717, 's_col': 4722, 's_2206': 4733, 's_txt': 4734, 's_split': None, 'n_pos': 4738, 'n_col': 4743, 'n_2206': 4754, 'n_txt': 4755, 'n_split': 4760, 'd_recs': [4805], 't_recs': [4780, 4785]},
    16: {'s_pos': 4889, 's_col': 4894, 's_2206': 4905, 's_txt': 4906, 's_split': None, 'n_pos': 4910, 'n_col': 4915, 'n_2206': 4926, 'n_txt': 4927, 'n_split': 4932, 'd_recs': [4982, 4987], 't_recs': [4952, 4957, 4962]},
    17: {'s_pos': 5036, 's_col': 5041, 's_2206': 5052, 's_txt': 5053, 's_split': None, 'n_pos': 5057, 'n_col': 5062, 'n_2206': 5073, 'n_txt': 5074, 'n_split': None, 'd_recs': [5119], 't_recs': [5094, 5099]},
    18: {'s_pos': 5204, 's_col': 5209, 's_2206': 5220, 's_txt': 5221, 's_split': None, 'n_pos': 5225, 'n_col': 5230, 'n_2206': 5241, 'n_txt': 5242, 'n_split': 5247, 'd_recs': [5287, 5292], 't_recs': [5267]},
    19: {'s_pos': 5336, 's_col': 5341, 's_2206': 5352, 's_txt': 5353, 's_split': None, 'n_pos': 5357, 'n_col': 5362, 'n_2206': 5373, 'n_txt': 5374, 'n_split': 5379, 'd_recs': [5419], 't_recs': [5399]}
}

print("=== VERIFYING ROW MAPPINGS ===")
for r_num, m in row_map_6707.items():
    s_txt = doc.records[m['s_txt']]['payload'].decode('utf-16le', errors='ignore')
    n_txt = doc.records[m['n_txt']]['payload'].decode('utf-16le', errors='ignore')
    n_spl = doc.records[m['n_split']]['payload'].decode('utf-16le', errors='ignore') if m['n_split'] else ''
    d_txt = " + ".join([doc.records[idx]['payload'].decode('utf-16le', errors='ignore') for idx in m['d_recs']])
    t_txt = " + ".join([doc.records[idx]['payload'].decode('utf-16le', errors='ignore') for idx in m['t_recs']])
    
    # Check tags
    assert doc.records[m['s_pos']]['tag'] == 2100, f"Row {r_num} s_pos tag {doc.records[m['s_pos']]['tag']} != 2100"
    assert doc.records[m['s_col']]['tag'] == 150,  f"Row {r_num} s_col tag {doc.records[m['s_col']]['tag']} != 150"
    assert doc.records[m['s_2206']]['tag'] == 2206, f"Row {r_num} s_2206 tag {doc.records[m['s_2206']]['tag']} != 2206"
    assert doc.records[m['s_txt']]['tag'] in (2201, 2202), f"Row {r_num} s_txt tag error"
    
    assert doc.records[m['n_pos']]['tag'] == 2100, f"Row {r_num} n_pos tag {doc.records[m['n_pos']]['tag']} != 2100"
    assert doc.records[m['n_col']]['tag'] == 150,  f"Row {r_num} n_col tag {doc.records[m['n_col']]['tag']} != 150"
    assert doc.records[m['n_2206']]['tag'] == 2206, f"Row {r_num} n_2206 tag {doc.records[m['n_2206']]['tag']} != 2206"
    assert doc.records[m['n_txt']]['tag'] in (2201, 2202), f"Row {r_num} n_txt tag error"
    
    print(f"Row {r_num:2d}: Saldo='{s_txt}' Nominal='{n_txt}{n_spl}' Date='{d_txt}' Time='{t_txt}' [PASS]")

print("\n100% OF 19 ROWS FULLY VERIFIED AND VALIDATED!")
