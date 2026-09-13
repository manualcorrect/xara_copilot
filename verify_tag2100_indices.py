from xar_dom_engine import XarDocument
from compare_test3_with_user_table import found_pairs
import struct

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# Inspect Tag 2100 and Tag 2206 for rows 29 to 36
for row_idx in range(29, 37):
    s_story = found_pairs[1 + (row_idx - 1)*2]
    n_story = found_pairs[1 + (row_idx - 1)*2 + 1]
    
    # Saldo
    s_t2100_idx = None
    s_t2206_idx = None
    for j in range(s_story[1]-20, s_story[1]):
        if doc.records[j]['tag'] == 2100 and len(doc.records[j]['payload']) == 12:
            s_t2100_idx = j
    for j in range(s_story[1], s_story[2]+1):
        if doc.records[j]['tag'] == 2206 and len(doc.records[j]['payload']) == 12:
            s_t2206_idx = j
            
    # Nominal
    n_t2100_idx = None
    n_t2206_idx = None
    for j in range(n_story[1]-20, n_story[1]):
        if doc.records[j]['tag'] == 2100 and len(doc.records[j]['payload']) == 12:
            n_t2100_idx = j
    for j in range(n_story[1], n_story[2]+1):
        if doc.records[j]['tag'] == 2206 and len(doc.records[j]['payload']) == 12:
            n_t2206_idx = j
            
    s_p2100 = struct.unpack('<iii', doc.records[s_t2100_idx]['payload'])
    s_p2206 = struct.unpack('<iii', doc.records[s_t2206_idx]['payload'])
    n_p2100 = struct.unpack('<iii', doc.records[n_t2100_idx]['payload'])
    n_p2206 = struct.unpack('<iii', doc.records[n_t2206_idx]['payload'])
    
    print(f"Row {row_idx:2d}:")
    print(f"  Saldo   (Story {s_story[1]}): Tag 2100 Rec {s_t2100_idx} {s_p2100} | Tag 2206 Rec {s_t2206_idx} {s_p2206}")
    print(f"  Nominal (Story {n_story[1]}): Tag 2100 Rec {n_t2100_idx} {n_p2100} | Tag 2206 Rec {n_t2206_idx} {n_p2206}")
