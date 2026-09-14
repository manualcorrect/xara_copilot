import os
import struct
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== NAME BLOCKS SCAN IN AUG/0.XAR ===")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'ROY DARWIN' in txt:
            # find enclosing story start (tag 2100) and end (tag 2203)
            story_start = None
            for k in range(max(0, i-40), i):
                if doc.records[k]['tag'] == 2100:
                    story_start = k
            story_end = None
            for k in range(i, min(len(doc.records), i+30)):
                if doc.records[k]['tag'] == 2203:
                    story_end = k
                    break
            print(f"Name text at {i} ({txt!r}): story_start={story_start}, story_end={story_end}")
            if story_start:
                for s in range(story_start, (story_end or i) + 5):
                    rs = doc.records[s]
                    pl_info = f"len={len(rs['payload'])}"
                    if rs['tag'] in (2201, 2202):
                        pl_info += f" text={rs['payload'].decode('utf-16le', errors='ignore')!r}"
                    elif rs['tag'] == 2100:
                        coords = struct.unpack(f'<{len(rs["payload"])//4}i', rs['payload'])
                        pl_info += f" coords={coords}"
                    elif rs['tag'] == 2150:
                        w, fl = struct.unpack('<iB', rs['payload'])
                        pl_info += f" w={w}, flag={fl}"
                    elif rs['tag'] == 2206:
                        t2206_val = struct.unpack('<iii', rs['payload'][:12])
                        pl_info += f" dx,dy,dz={t2206_val}"
                    elif rs['tag'] in (150, 2901, 2906, 2907, 4208, 4209):
                        pl_info += f" hex={rs['payload'].hex()}"
                    print(f"   [{s:5d}] Tag {rs['tag']:4d}: {pl_info}")
