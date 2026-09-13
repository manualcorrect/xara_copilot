from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1.xar'
doc = XarDocument(target_file)
print(f"Total records: {len(doc.records)}")

# Find text stories and search for names
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            s = r['payload'].decode('utf-16le', errors='ignore').strip('\x00')
            if any(k in s.lower() for k in ['nama', 'cabang', 'kcp', 'branch', 'dini', 'anwar', 'asep', 'khodijah']):
                print(f"Rec {i} Tag {r['tag']}: {repr(s)}")
        except Exception:
            pass
