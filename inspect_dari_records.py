from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap4.xar'
doc = XarDocument(target_file)
print(f"Total records: {len(doc.records)}")

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
        if 'ari' in s and len(s) <= 8 and not any(k in s.lower() for k in ['jan', 'syari', 'aladi']):
            print(f"Rec {i:05d} Tag {r['tag']:04d}: {repr(s)}")
            for k in range(i-3, i+6):
                r2 = doc.records[k]
                if r2['tag'] in (2201, 2202):
                    print(f"   [{k:05d}] Tag {r2['tag']:04d} len={len(r2['payload']):02d}: {repr(r2['payload'].decode('utf-16le', errors='replace').strip('\x00'))}")
