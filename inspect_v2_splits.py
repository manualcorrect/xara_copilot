from xar_dom_engine import XarDocument
import os

v2_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar'
if os.path.exists(v2_file):
    doc = XarDocument(v2_file)
    print("Loaded test_v2.1_tahap7.xar")
    for i, r in enumerate(doc.records):
        if r['tag'] in (2201, 2202) and len(r['payload']) <= 4:
            print(f"Rec {i}: Tag {r['tag']}, len={len(r['payload'])}, payload={repr(r['payload'])}")
