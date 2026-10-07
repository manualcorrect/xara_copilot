from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap4.xar'
doc = XarDocument(target_file)
print(f"Total records: {len(doc.records)}")

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
        if any(k in s.lower() for k in ['dari', 'of 5', ' of ']):
            print(f"Rec {i:05d} Tag {r['tag']:04d} len={len(r['payload']):02d}: {repr(s)}")
            # print surrounding text records
            for k in range(max(0, i-5), min(len(doc.records), i+6)):
                if doc.records[k]['tag'] in (2201, 2202):
                    s2 = doc.records[k]['payload'].decode('utf-16le', errors='replace').strip('\x00')
                    print(f"   [{k:05d}] {repr(s2)}")
