from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap3.xar'
doc = XarDocument(target_file)
print(f"Total records: {len(doc.records)}")

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
        digits = [c for c in s if c.isdigit()]
        if len(digits) >= 10 and ',' not in s:
            print(f"Rec {i:05d} Tag {r['tag']:04d} len={len(r['payload']):02d}: {repr(s)}")
