from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(target_file)

# Let's find all text blocks in the table
# A transaction row typically starts with a time or date, description, amount, balance.
# Let's inspect all text records with their index and decoded string.
rows = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if any(m in s for m in ['Apr 2025', 'Apr 202', ' Apr 202', 'Apr 20', '2025']) or ('Apr' in s):
            # Check context
            prev_txt = [(j, doc.records[j]['payload'].decode('utf-16le', errors='replace')) for j in range(max(0, i-10), i) if doc.records[j]['tag'] in (2201, 2202)]
            next_txt = [(j, doc.records[j]['payload'].decode('utf-16le', errors='replace')) for j in range(i+1, min(len(doc.records), i+10)) if doc.records[j]['tag'] in (2201, 2202)]
            rows.append((i, r['tag'], s, prev_txt, next_txt))

print(f"Total date matches found: {len(rows)}")
for idx, tag, s, prev_t, next_t in rows:
    print(f"\nRecord {idx} [Tag {tag}]: {repr(s)}")
    print(f"  Prev: {prev_t[-2:] if prev_t else []}")
    print(f"  Next: {next_t[:2] if next_t else []}")
