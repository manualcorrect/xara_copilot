from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(target_file)

for i in range(4375, 4420):
    r = doc.records[i]
    tag = r['tag']
    txt = ""
    if tag in (2201, 2202):
        txt = repr(r['payload'].decode('utf-16le', errors='replace'))
    print(f"{i}: Tag {tag} (len={len(r['payload'])}) {txt}")
