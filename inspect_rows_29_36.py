from compare_test3_with_user_table import found_pairs, user_table
from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# Inspect Rows 29 to 36 in full detail
for row_idx in range(29, 37):
    s_story = found_pairs[1 + (row_idx - 1)*2]
    n_story = found_pairs[1 + (row_idx - 1)*2 + 1]
    u_row, u_nom, u_sal = user_table[row_idx - 1]
    
    print(f"\n=================== ROW {row_idx} ===================")
    print(f"User Target: Nominal={u_nom}, Saldo={u_sal}")
    print(f"SALDO STORY (recs {s_story[1]}..{s_story[2]}):")
    for rec_i in range(s_story[1], s_story[2]+1):
        r = doc.records[rec_i]
        txt = repr(r['payload'].decode('utf-16le', errors='replace')) if r['tag'] in (2201, 2202) else f"len={len(r['payload'])}"
        print(f"  {rec_i:5d}: Tag {r['tag']:4d} {txt}")
        
    print(f"NOMINAL STORY (recs {n_story[1]}..{n_story[2]}):")
    for rec_i in range(n_story[1], n_story[2]+1):
        r = doc.records[rec_i]
        txt = repr(r['payload'].decode('utf-16le', errors='replace')) if r['tag'] in (2201, 2202) else f"len={len(r['payload'])}"
        print(f"  {rec_i:5d}: Tag {r['tag']:4d} {txt}")
