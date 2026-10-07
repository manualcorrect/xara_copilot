from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(target_file)
print(f"Total records: {len(doc.records)}")

date_records = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if 'Apr 2025' in s:
            date_records.append((i, r['tag'], len(r['payload']), repr(s)))

print(f"Total date records with Apr 2025: {len(date_records)}")
for d in date_records:
    print(d)
