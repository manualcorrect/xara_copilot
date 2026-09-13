from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap1.xar'
doc = XarDocument(target_file)
print(f"Total records: {len(doc.records)}")

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
        if any(k in s.lower() for k in ['periode', 'period', 'apr 2025', 'mar 2025', '2025', '2026', ' - ']):
            print(f"Rec {i:05d} Tag {r['tag']:04d} len={len(r['payload']):03d}: {repr(s)}")
