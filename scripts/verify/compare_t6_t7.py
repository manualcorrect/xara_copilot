import struct
from xar_dom_engine import XarDocument

MP_PER_CM = 72000 / 2.54

doc6 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap6.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

# Let's compare Row 1 and Row 2 in doc6 vs doc7
for r_name, doc in [("TAHAP 6", doc6), ("TAHAP 7", doc7)]:
    print(f"\n=== {r_name} ===")
    for k in [1548, 1564, 1565, 1527, 1543, 1544, 1739, 1755, 1756, 1695, 1710, 1711]:
        tag = doc.records[k]['tag']
        p = doc.records[k]['payload']
        if tag == 2100:
            ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
            print(f"[{k}] 2100 (Matrix): X={ints[0]} ({ints[0]/MP_PER_CM:.3f} cm)")
        elif tag == 2206:
            ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
            print(f"[{k}] 2206: ints={ints}")
        elif tag == 2201:
            txt = p.decode('utf-16le', errors='replace')
            print(f"[{k}] 2201: '{txt}'")
