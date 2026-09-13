import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

def print_fonts(path, name):
    print(f"\n=== {name} ===")
    doc = XarDocument(path)
    for i, r in enumerate(doc.records):
        if r['tag'] == 2000:
            p = r['payload']
            handle = struct.unpack('<i', p[:4])[0] if len(p) >= 4 else 0
            # decode text inside payload
            # text in Tag 2000 has 2 names: font name and style
            # let's see how string is formatted
            txt = p[4:].decode('utf-16le', errors='replace')
            print(f"Rec [{i:4d}] Tag 2000: Handle={handle} ({hex(handle)}) | Payload={repr(txt[:60])}")

print_fonts(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar', 'test_3.1.xar')
print_fonts(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar', 'test_v2.1_tahap7.xar')
