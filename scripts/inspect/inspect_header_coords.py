from xar_dom_engine import XarDocument
import struct

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

for i in range(1250, 1315):
    r = doc.records[i]
    tag = r['tag']
    if tag in (2100, 2206, 2201, 2202):
        if tag in (2201, 2202):
            txt = repr(r['payload'].decode('utf-16le', errors='replace'))
        else:
            txt = struct.unpack('<iii', r['payload']) if len(r['payload']) == 12 else f"len={len(r['payload'])}"
        print(f"{i:4d}: Tag {tag:4d} {txt}")
