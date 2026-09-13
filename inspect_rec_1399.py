from xar_dom_engine import XarDocument

t6_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
t7_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7.xar'

d6 = XarDocument(t6_file)
d7 = XarDocument(t7_file)

print("=== TAHAP 6 around 1399 ===")
for i in range(1385, 1415):
    r = d6.records[i]
    tag = r['tag']
    txt = repr(r['payload'].decode('utf-16le', errors='replace')) if tag in (2201, 2202) else f"len={len(r['payload'])}"
    print(f"{i}: Tag {tag} {txt}")

print("\n=== TAHAP 7 around 1399 ===")
for i in range(1385, 1415):
    r = d7.records[i]
    tag = r['tag']
    txt = repr(r['payload'].decode('utf-16le', errors='replace')) if tag in (2201, 2202) else f"len={len(r['payload'])}"
    print(f"{i}: Tag {tag} {txt}")
