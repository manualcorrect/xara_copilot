import struct
from xar_dom_engine import XarDocument

MP_PER_CM = 72000 / 2.54

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

print("=== SPREAD & PAGE RECORDS ===")
for i, r in enumerate(doc.records):
    if r['tag'] in [43, 45]:
        p = r['payload']
        ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4]) if len(p) >= 4 else ()
        print(f"[{i}] Tag {r['tag']}: ints={ints}")

