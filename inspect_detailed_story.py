import struct
from xar_dom_engine import XarDocument

MP_PER_CM = 72000 / 2.54

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

table_master = [
    (1, 1565, 1544),
    (2, 1756, 1711),
    (3, 2016, 1958),
    (4, 2189, 2154),
    (5, 2352, 2331),
    (6, 2495, 2442),
    (7, 2657, 2631),
    (8, 2842, 2811),
    (9, 2944, 2923),
    (10, 3051, 3030),
    (11, 4425, 4381),
    (12, 4549, 4505),
    (13, 4767, 4706),
    (14, 4983, 4948),
    (15, 6405, 6361),
    (16, 6598, 6554),
    (17, 6740, 6719)
]

print("=== DETAILED STORY STRUCTURE ACROSS ALL 17 ROWS ===")
for r_num, nom_idx, sal_idx in table_master:
    # Look back 25 records from nom_idx
    print(f"\n--- ROW {r_num} ---")
    for name, target_idx in [("NOMINAL", nom_idx), ("SALDO", sal_idx)]:
        records_in_story = []
        for k in range(max(0, target_idx - 25), min(len(doc.records), target_idx + 5)):
            tag = doc.records[k]['tag']
            payload = doc.records[k]['payload']
            if tag == 2100:
                ints = struct.unpack(f"<{len(payload)//4}i", payload[:(len(payload)//4)*4])
                records_in_story.append(f"[{k}] 2100 (Matrix: X={ints[0]}, Y={ints[1]})")
            elif tag == 2206:
                ints = struct.unpack(f"<{len(payload)//4}i", payload[:(len(payload)//4)*4])
                records_in_story.append(f"[{k}] 2206 (KX={ints[0]}, KY={ints[1]})")
            elif tag == 2201:
                txt = payload.decode('utf-16le', errors='replace').strip('\x00')
                records_in_story.append(f"[{k}] 2201 (Str: '{txt}')")
            elif tag == 2202:
                txt = payload.decode('utf-16le', errors='replace').strip('\x00')
                records_in_story.append(f"[{k}] 2202 (Char: '{txt}')")
            elif tag == 2204:
                ints = struct.unpack(f"<{len(payload)//4}i", payload[:(len(payload)//4)*4])
                records_in_story.append(f"[{k}] 2204 (Kern: ints={ints})")
        print(f"  [{name}]: " + " -> ".join(records_in_story))
