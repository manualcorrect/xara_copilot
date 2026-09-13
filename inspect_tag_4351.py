import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

def inspect_tag_4351(path, name):
    print(f"\n=== TAG 4351 in {name} ===")
    doc = XarDocument(path)
    for i, r in enumerate(doc.records[:600]):
        if r['tag'] == 4351:
            p = r['payload']
            ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
            print(f"Rec [{i:4d}] Tag 4351 len={len(p)}: ints={ints[:10]} (total {len(ints)} ints)")

inspect_tag_4351(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar', 'test_3.1.xar')
inspect_tag_4351(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar', 'test_v2.1_tahap7.xar')
