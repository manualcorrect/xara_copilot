import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

def list_font_glyphs(path, name, target_fid):
    print(f"\n=== Glyphs for FontID {target_fid} in {name} ===")
    doc = XarDocument(path)
    glyphs = []
    for i, r in enumerate(doc.records):
        if r['tag'] == 4350 and len(r['payload']) >= 6:
            fid = struct.unpack('<I', r['payload'][:4])[0]
            if fid == target_fid:
                char_code = struct.unpack('<H', r['payload'][4:6])[0]
                char_str = chr(char_code) if 32 <= char_code <= 126 else f"\\u{char_code:04X}"
                glyphs.append((i, char_str, char_code, len(r['payload'])))
    print(f"Total glyphs: {len(glyphs)}")
    for rec_idx, c_str, c_code, plen in glyphs:
        print(f"  Rec [{rec_idx:4d}] Char '{c_str}' (0x{c_code:04X}) len={plen}")

list_font_glyphs(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar', 'test_3.1.xar', 13)
list_font_glyphs(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar', 'test_v2.1_tahap7.xar', 13)
