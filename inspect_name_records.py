from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1.xar'
doc = XarDocument(target_file)

for idx in [1023, 3823, 6829, 9772, 12656]:
    print(f"\n=== Around Record {idx} ===")
    for k in range(idx - 3, idx + 16):
        r = doc.records[k]
        val = r['payload'].decode('utf-16le', errors='replace') if r['tag'] in (2201, 2202) else r['payload'].hex()[:20]
        print(f"{k:05d} Tag {r['tag']:04d} len={len(r['payload']):03d}: {repr(val)}")
