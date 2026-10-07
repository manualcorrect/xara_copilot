from xar_dom_engine import XarDocument
from compare_test3_with_user_table import found_pairs
import struct

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# Check rows 23 to 38
for row_idx in range(23, 39):
    s_story = found_pairs[1 + (row_idx - 1)*2]
    n_story = found_pairs[1 + (row_idx - 1)*2 + 1]
    
    # Get Tag 2100 and Tag 2206 for Saldo
    s_t2100 = None
    s_t2206 = None
    for j in range(s_story[1]-20, s_story[1]):
        if doc.records[j]['tag'] == 2100 and len(doc.records[j]['payload']) == 12:
            s_t2100 = struct.unpack('<iii', doc.records[j]['payload'])
    for j in range(s_story[1], s_story[2]+1):
        if doc.records[j]['tag'] == 2206 and len(doc.records[j]['payload']) == 12:
            s_t2206 = struct.unpack('<iii', doc.records[j]['payload'])
            
    # Get Tag 2100 and Tag 2206 for Nominal
    n_t2100 = None
    n_t2206 = None
    for j in range(n_story[1]-20, n_story[1]):
        if doc.records[j]['tag'] == 2100 and len(doc.records[j]['payload']) == 12:
            n_t2100 = struct.unpack('<iii', doc.records[j]['payload'])
    for j in range(n_story[1], n_story[2]+1):
        if doc.records[j]['tag'] == 2206 and len(doc.records[j]['payload']) == 12:
            n_t2206 = struct.unpack('<iii', doc.records[j]['payload'])
            
    s_xr = (s_t2100[0] + s_t2206[0]) if (s_t2100 and s_t2206) else None
    n_xr = (n_t2100[0] + n_t2206[0]) if (n_t2100 and n_t2206) else None
    
    print(f"Row {row_idx:2d}:")
    print(f"  Saldo   ({s_story[3]:14s}): X={s_t2100[0] if s_t2100 else None}, W={s_t2206[0] if s_t2206 else None} -> X_right={s_xr}")
    print(f"  Nominal ({n_story[3]:14s}): X={n_t2100[0] if n_t2100 else None}, W={n_t2206[0] if n_t2206 else None} -> X_right={n_xr}")
