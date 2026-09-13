from xar_dom_engine import XarDocument
import re

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

print(f"Total records in test_3.1_tahap6.xar: {len(doc.records)}")

# 1. Look for Header Summary around records 1000-1400 (Page 1)
print("\n=== HEADER SUMMARY CANDIDATES ===")
for i in range(1000, 1400):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        s = r['payload'].decode('utf-16le', errors='replace')
        if any(c in s for c in ['00', 'Saldo', 'Dana', 'Awal', 'Akhir']) or re.search(r'\d+\.\d+', s):
            print(f"Rec {i:4d} [Tag {r['tag']}]: {repr(s)}")
