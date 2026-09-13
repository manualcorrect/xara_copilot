from xar_dom_engine import XarDocument
import struct

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

for j in range(8315, 8335):
    r = doc.records[j]
    if r['tag'] == 2100:
        print(f"{j}: Tag 2100 payload={struct.unpack('<iii', r['payload'])}")
    else:
        print(f"{j}: Tag {r['tag']}")
