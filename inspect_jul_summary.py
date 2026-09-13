import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

print("=== SUMMARY NODES INSPECTION ===")
for r_idx in [1142, 1163, 1164, 1169, 1176, 1181, 1468, 1473]:
    r = doc.records[r_idx]
    txt = r['payload'].decode('utf-16le').rstrip('\x00')
    print(f"Rec {r_idx}: Tag={r['tag']} Text='{txt}'")
    # check nearby tags 2206, 2100, 150
    for j in range(max(0, r_idx-15), min(len(doc.records), r_idx+5)):
        rec = doc.records[j]
        if rec['tag'] in (2206, 2100, 150):
            if rec['tag'] == 150:
                print(f"   Near {j}: Tag 150 col={rec['payload'].hex()}")
            else:
                vals = struct.unpack('<iii', rec['payload'][:12])
                print(f"   Near {j}: Tag {rec['tag']} vals={vals}")
