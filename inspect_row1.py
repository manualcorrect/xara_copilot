from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

print("=== INSPECTING 1650 to 1720 ===")
for i in range(1650, 1720):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        print(f"Rec {i:4d} [Tag {r['tag']}]: {repr(s)}")
