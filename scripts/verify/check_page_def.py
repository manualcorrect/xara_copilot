import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

print("=== CHECK PAGE DEFINITIONS & SPREAD ===")
for i, r in enumerate(doc.records[:100]):
    # Tag 2007 (TAG_SPREAD), Tag 2008 (TAG_PAGE), Tag 2009 (TAG_LAYER), Tag 2010 etc.
    if r['tag'] in [2007, 2008, 2009, 2010, 2011, 2012]:
        p = r['payload']
        ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4]) if len(p) >= 4 else ()
        print(f"[{i}] Tag {r['tag']}: ints={ints}")

