import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

doc3 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

print("=== FONT ID 13 (BOLD) IN TEST 3.1 ===")
for i in range(334, 392):
    r = doc3.records[i]
    tag = r['tag']
    p = r['payload']
    ch = ""
    if tag == 4350:
        fid = struct.unpack('<I', p[:4])[0]
        c = struct.unpack('<H', p[4:6])[0]
        ch = f"FID={fid} Char='{chr(c) if 32<=c<=126 else hex(c)}'"
    elif tag == 4351:
        ints = struct.unpack(f"<{min(len(p)//4, 4)}i", p[:min(len(p)//4, 4)*4])
        ch = f"KERNING ints={ints}"
    elif tag == 2000:
        ch = f"FONT_DEF '{p[4:].decode('utf-16le', errors='replace').split(chr(0))[0]}'"
    print(f"[{i:4d}] Tag={tag} len={len(p):4d} : {ch}")

print("\n=== FONT ID 13 (BOLD) IN TAHAP 7 ===")
for i in range(324, 380):
    r = doc7.records[i]
    tag = r['tag']
    p = r['payload']
    ch = ""
    if tag == 4350:
        fid = struct.unpack('<I', p[:4])[0]
        c = struct.unpack('<H', p[4:6])[0]
        ch = f"FID={fid} Char='{chr(c) if 32<=c<=126 else hex(c)}'"
    elif tag == 4351:
        ints = struct.unpack(f"<{min(len(p)//4, 4)}i", p[:min(len(p)//4, 4)*4])
        ch = f"KERNING ints={ints}"
    elif tag == 2000:
        ch = f"FONT_DEF '{p[4:].decode('utf-16le', errors='replace').split(chr(0))[0]}'"
    print(f"[{i:4d}] Tag={tag} len={len(p):4d} : {ch}")
