from compare_test3_with_user_table import user_table, found_pairs

# found_pairs[0] is header summary
# found_pairs[1..] are the 47 pairs
diffs = []
for row_idx in range(1, 48):
    saldo_story = found_pairs[1 + (row_idx - 1)*2]
    nominal_story = found_pairs[1 + (row_idx - 1)*2 + 1]
    
    file_saldo = saldo_story[3]
    file_nominal = nominal_story[3]
    
    u_row, u_nom, u_saldo = user_table[row_idx - 1]
    
    saldo_match = (file_saldo == u_saldo)
    nominal_match = (file_nominal == u_nom)
    
    if not (saldo_match and nominal_match):
        diffs.append({
            'row': row_idx,
            'file_nom': file_nominal,
            'user_nom': u_nom,
            'file_sal': file_saldo,
            'user_sal': u_saldo,
            'nom_match': nominal_match,
            'sal_match': saldo_match,
            'saldo_recs': saldo_story[4],
            'nominal_recs': nominal_story[4],
            'saldo_story_start': saldo_story[1],
            'nominal_story_start': nominal_story[1]
        })

print(f"Total rows differing from user table: {len(diffs)}")
for d in diffs:
    print(f"\nRow {d['row']:2d}:")
    print(f"  Nominal: File={repr(d['file_nom']):16s} vs User={repr(d['user_nom']):16s} (Match: {d['nom_match']})")
    print(f"  Saldo  : File={repr(d['file_sal']):16s} vs User={repr(d['user_sal']):16s} (Match: {d['sal_match']})")
