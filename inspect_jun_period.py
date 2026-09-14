import os
import struct
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
p7 = os.path.join(folder, '0_tahap7.xar')

doc7 = XarDocument(p7)
print("=== PERIOD HEADERS IN JUN 0_TAHAP7.XAR ===")
for i, r in enumerate(doc7.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Jun 2026' in txt and '-' in txt:
            print(f"\n--- Period Main Node at Rec {i} ({txt!r}) ---")
            for k in range(max(0, i-15), min(len(doc7.records), i+10)):
                rk = doc7.records[k]
                extra = ""
                if rk['tag'] in (2201, 2202):
                    extra = f"TEXT: {rk['payload'].decode('utf-16le', errors='ignore')!r}"
                print(f"  [{k:5d}] Tag {rk['tag']:4d}: {extra}")
