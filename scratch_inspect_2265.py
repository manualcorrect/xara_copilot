import struct
from xar_dom_engine import XarDocument

file_path = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_2_clean.pdf.xar'
doc = XarDocument(file_path)

print("=== RECS 2265..2315 IN test_2_clean.pdf.xar ===")
for i in range(2265, 2315):
    r = doc.records[i]
    tag = r['tag']
    p = r['payload']
    desc = f"Tag {tag:4d} (len={len(p)})"
    if tag == 2100:
        desc += f" Matrix: {struct.unpack('<iii', p[:12])}"
    elif tag == 2206:
        desc += f" Advance: {struct.unpack('<iii', p[:12])}"
    elif tag in (2201, 2202):
        desc += f" Text: {repr(p.decode('utf-16le', errors='ignore'))}"
    elif tag == 2204:
        desc += f" Kern: {struct.unpack('<ii', p[:8])}"
    elif tag == 2200:
        desc += " [Story Start]"
    elif tag == 2203:
        desc += " [EOL]"
    print(f"[{i:4d}] {desc}")
