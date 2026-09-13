import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

def inspect_fonts(path, name):
    doc = XarDocument(path)
    print(f"\n=======================================================")
    print(f"FONTS IN {name}")
    print(f"=======================================================")
    
    # Check font definition records (Tag 2000, 2001, etc.)
    for i, r in enumerate(doc.records):
        tag = r['tag']
        p = r['payload']
        # Check Tag 2000 (TAG_FONT_DEF) or Tag 4350 / 4351
        if tag in [2000, 2001, 2002, 4350, 4351]:
            desc = ""
            if tag == 2000:
                # payload usually has font handle / ID and font name
                handle = struct.unpack('<i', p[:4])[0] if len(p) >= 4 else 0
                font_name = p[4:].decode('ascii', errors='replace').strip('\x00')
                desc = f"FONT_DEF: Handle={handle} (0x{handle:04X}) Name='{font_name}'"
            elif tag in [4350, 4351]:
                desc = f"EMBEDDED_FONT_DATA (len={len(p)})"
            print(f"[{i:4d}] Tag={tag} : {desc}")

inspect_fonts(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar', 'test_3.1.xar')
inspect_fonts(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar', 'test_v2.1_tahap7.xar')
