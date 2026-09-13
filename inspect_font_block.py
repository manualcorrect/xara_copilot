import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

print("=== RECORDS 375 to 450 IN TAHAP 7 ===")
for i in range(374, 450):
    r = doc7.records[i]
    tag = r['tag']
    p = r['payload']
    desc = ""
    if tag == 2000:
        desc = f"FONT_DEF '{p[4:].decode('utf-16le', errors='replace').split(chr(0))[0]}'"
    elif tag == 4350:
        fid = struct.unpack('<I', p[:4])[0] if len(p)>=4 else 0
        c = struct.unpack('<H', p[4:6])[0] if len(p)>=6 else 0
        desc = f"GLYPH FID={fid} '{chr(c) if 32<=c<=126 else hex(c)}'"
    elif tag == 4351:
        desc = f"KERNING len={len(p)}"
    elif tag in [2901, 2902, 2906, 2907, 2908, 150, 4352]:
        desc = f"ATTR tag={tag} len={len(p)}"
    print(f"[{i:4d}] Tag={tag:4d} len={len(p):4d} : {desc}")
