from xar_dom_engine import XarDocument
from verify_user_table import transactions as user_table

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7.xar'
doc = XarDocument(target_file)

# Extract only table transaction stories (i > 1400)
found_pairs = []
i = 0
while i < len(doc.records):
    r = doc.records[i]
    if r['tag'] == 2200 and i > 1400: # Only transaction table area
        story_recs = []
        j = i + 1
        while j < len(doc.records) and doc.records[j]['tag'] != 2203:
            if doc.records[j]['tag'] in (2201, 2202):
                story_recs.append((j, doc.records[j]['tag'], doc.records[j]['payload'].decode('utf-16le', errors='replace')))
            j += 1
        story_text = "".join(sr[2] for sr in story_recs).strip()
        if (story_text.startswith('+') or story_text.startswith('-')) and any(c.isdigit() for c in story_text) and not ('Dec' in story_text or 'e-Statement' in story_text):
            found_pairs.append(('NOMINAL', i, j, story_text, story_recs))
        elif any(c in story_text for c in [',00', ',0', ',']) and any(c.isdigit() for c in story_text) and not any(w in story_text for w in ['Dec', 'Jan', 'Kav', '12190', 'Saldo', 'Dana', '163000', 'e-Statement']):
            found_pairs.append(('SALDO', i, j, story_text, story_recs))
        i = j
    else:
        i += 1

print(f"Total transaction stories extracted: {len(found_pairs)}")
assert len(found_pairs) == 94, f"Expected 94 stories (47 pairs), got {len(found_pairs)}"

all_pass = True
for row_idx in range(1, 48):
    saldo_story = found_pairs[(row_idx - 1)*2]
    nominal_story = found_pairs[(row_idx - 1)*2 + 1]
    
    file_saldo = saldo_story[3]
    file_nominal = nominal_story[3]
    
    ttype, exp_nom, exp_sal = user_table[row_idx - 1]
    expected_nominal = f"{ttype}{exp_nom}"
    expected_saldo = exp_sal
    
    nom_ok = (file_nominal == expected_nominal)
    sal_ok = (file_saldo == expected_saldo)
    
    if not (nom_ok and sal_ok):
        all_pass = False
        print(f"FAILED Row {row_idx:2d}:")
        print(f"  Nominal: File={file_nominal} vs Expected={expected_nominal}")
        print(f"  Saldo  : File={file_saldo} vs Expected={expected_saldo}")
    else:
        print(f"Row {row_idx:2d}: Nominal={file_nominal:>14s} | Saldo={file_saldo:>14s} [100% MATCH]")

assert all_pass, "Some rows failed verification!"
print("\n" + "="*60)
print("100% OF ALL 47 TRANSACTION ROWS MATCH USER TABLE PRECISELY!")
print("="*60)
