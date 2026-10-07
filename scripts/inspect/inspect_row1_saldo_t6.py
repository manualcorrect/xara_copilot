import struct
from xar_dom_engine import XarDocument

doc6 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap6.xar')

# Inspect all records from 1520 to 1550 (Row 1 Saldo)
print("=== ROW 1 SALDO IN TAHAP 6 ===")
for i in range(1520, 1550):
    r = doc6.records[i]
    tag = r['tag']
    p = r['payload']
    desc = ""
    if tag == 2100:
        ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
        desc = f"MATRIX ints={ints}"
    elif tag == 2206:
        ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
        desc = f"TAG_2206 ints={ints}"
    elif tag == 2201:
        desc = f"STR: '{p.decode('utf-16le', errors='replace')}'"
    elif tag == 2202:
        desc = f"CHAR: '{p.decode('utf-16le', errors='replace')}'"
    elif tag == 2204:
        ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
        desc = f"KERN ints={ints}"
    if desc:
        print(f"[{i:4d}] Tag={tag:4d} : {desc}")
