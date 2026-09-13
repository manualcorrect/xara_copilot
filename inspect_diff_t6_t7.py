from xar_dom_engine import XarDocument

t6_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
t7_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7.xar'

d6 = XarDocument(t6_file)
d7 = XarDocument(t7_file)

diff_recs = []
for i in range(len(d6.records)):
    r6 = d6.records[i]
    r7 = d7.records[i]
    if r6['tag'] != r7['tag'] or r6['payload'] != r7['payload'] or r6['size'] != r7['size']:
        diff_recs.append(i)

print(f"Total diff records: {len(diff_recs)}")
print(f"First 10 diff records: {diff_recs[:10]}")
for i in diff_recs:
    t = d6.records[i]['tag']
    txt6 = repr(d6.records[i]['payload'].decode('utf-16le', errors='replace')) if t in (2201, 2202) else f"len={len(d6.records[i]['payload'])}"
    txt7 = repr(d7.records[i]['payload'].decode('utf-16le', errors='replace')) if t in (2201, 2202) else f"len={len(d7.records[i]['payload'])}"
    print(f"Rec {i:5d} [Tag {t:4d}]: t6={txt6} -> t7={txt7}")
