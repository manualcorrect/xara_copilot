import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

def find_char_glyphs(path, name):
    print(f"\n==================== GLYPHS IN {name} ====================")
    doc = XarDocument(path)
    current_font = "None"
    current_fid = -1
    for i, r in enumerate(doc.records):
        tag = r['tag']
        p = r['payload']
        if tag == 2000:
            txt = p[4:].decode('utf-16le', errors='replace').split('\x00')[0]
            current_font = txt
            print(f"\n[{i:4d}] FONT_DEF: '{current_font}'")
        elif tag in [4350, 4351]:
            if len(p) >= 6:
                fid = struct.unpack('<I', p[:4])[0]
                char_code = struct.unpack('<H', p[4:6])[0]
                char_str = chr(char_code) if 32 <= char_code <= 126 else f"\\u{char_code:04X}"
                # If it's a digit:
                if '0' <= char_str <= '9':
                    print(f"  [{i:4d}] Tag={tag} len={len(p):4d} : FontID={fid} Char='{char_str}' (0x{char_code:04X}) bytes[:8]={p[:8].hex()}")

find_char_glyphs(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar', 'test_3.1.xar')
find_char_glyphs(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar', 'test_v2.1_tahap7.xar')
