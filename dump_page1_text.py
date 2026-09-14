import os
import struct
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

for i in range(500, 1300):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        t2100_info = ""
        for k in range(max(0, i-20), i):
            if doc.records[k]['tag'] == 2100:
                coords = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]["payload"])
                t2100_info = f" Pos: {coords}"
        print(f"[{i:5d}] Tag {r['tag']}: {r['payload'].decode('utf-16le', errors='ignore')!r:35s}{t2100_info}")
