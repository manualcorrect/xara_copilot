from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')
print("=== Summary Block Texts ===")
for i in range(1130, 1205):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        print(f"Rec {i} Tag {r['tag']} (len={len(r['payload'])}): {repr(s)}")

print("\n=== Row 1 to Row 3 Texts ===")
for i in range(1520, 1780):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        print(f"Rec {i} Tag {r['tag']} (len={len(r['payload'])}): {repr(s)}")
