import struct
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== DETAILED PERIOD NODES ACROSS ALL 10 PAGES ===")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'Mar 202' in r['payload'].decode('utf-16le', errors='ignore') and '-' in r['payload'].decode('utf-16le', errors='ignore'):
        # found period main node
        print(f"\n--- Period Main Node at Rec {i} ---")
        for k in range(max(0, i-18), min(len(doc.records), i+12)):
            rk = doc.records[k]
            tag = rk['tag']
            pl = rk['payload']
            extra = ""
            if tag in (2201, 2202):
                extra = f"TEXT: {pl.decode('utf-16le', errors='ignore')!r}"
            elif tag == 2150:
                w, fl = struct.unpack('<iB', pl)
                extra = f"BOX: w={w}, flag={fl}"
            elif tag == 2206:
                t6 = struct.unpack('<iii', pl[:12])
                extra = f"T2206: {t6}"
            print(f"  [{k:5d}] Tag {tag:4d}: {extra}")
