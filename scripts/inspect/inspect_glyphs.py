import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

def inspect_glyphs(path, name):
    print(f"\n==================== {name} ====================")
    doc = XarDocument(path)
    
    # Track current font
    current_font = "None"
    for i in range(150, 500):
        r = doc.records[i]
        tag = r['tag']
        p = r['payload']
        if tag == 2000:
            txt = p[4:].decode('utf-16le', errors='replace').split('\x00')[0]
            current_font = txt
            print(f"\n[{i:4d}] FONT_DEF: '{current_font}'")
        elif tag in [4350, 4351]:
            # What is in payload? Let's check first 16 bytes
            # Usually: char code (unicode or ascii), or glyph index
            ints = struct.unpack(f"<{min(len(p)//4, 4)}i", p[:min(len(p)//4, 4)*4])
            # Is there a char?
            # Check if there's a 2-byte or 4-byte unicode character code
            char_guess = ""
            if len(p) >= 4:
                code = struct.unpack('<H', p[:2])[0]
                if 32 <= code <= 126:
                    char_guess = f"Char '{chr(code)}' (0x{code:04X})"
                else:
                    char_guess = f"Code 0x{code:04X} ({code})"
            print(f"  [{i:4d}] Tag={tag} len={len(p):4d} : {char_guess} | bytes[:8]={p[:8].hex()}")

inspect_glyphs(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar', 'test_3.1.xar')
