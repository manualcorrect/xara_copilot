from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

for i in range(1260, 1315):
    r = doc.records[i]
    tag = r['tag']
    txt = repr(r['payload'].decode('utf-16le', errors='replace')) if tag in (2201, 2202) else f"len={len(r['payload'])}"
    print(f"Rec {i:4d}: Tag {tag:4d} {txt}")
