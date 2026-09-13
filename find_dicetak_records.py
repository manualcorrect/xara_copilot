from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap2.xar'
doc = XarDocument(target_file)
print(f"Total records: {len(doc.records)}")

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
        if any(k in s.lower() for k in ['dicetak', 'issued on', 'issued']):
            print(f"Dicetak label at Rec {i:05d} Tag {r['tag']:04d}: {repr(s)}")
            # Show next 20 text records
            for k in range(i + 1, min(len(doc.records), i + 40)):
                if doc.records[k]['tag'] in (2201, 2202):
                    s2 = doc.records[k]['payload'].decode('utf-16le', errors='replace').strip('\x00')
                    print(f"   -> Rec {k:05d} Tag {doc.records[k]['tag']:04d} len={len(doc.records[k]['payload']):02d}: {repr(s2)}")
                    if any(m in s2.lower() for m in ['2025', '2026', '2027', 'may', 'apr', 'jan']):
                        break
