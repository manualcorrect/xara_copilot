import os
import struct
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
p7 = os.path.join(folder, '0_tahap7.xar')

doc7 = XarDocument(p7)
print(f"=== JUN 0_TAHAP7.XAR ({len(doc7.records):,} records) ===")

name_stories = []
mandiris = []

for i, r in enumerate(doc7.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'MASRIYAH' in txt:
            # find start tag 2100
            start = None
            for k in range(max(0, i-40), i):
                if doc7.records[k]['tag'] == 2100:
                    start = k
            # find end tag 2203
            end = None
            for k in range(i, min(len(doc7.records), i+30)):
                if doc7.records[k]['tag'] == 2203:
                    end = k + 1
                    while end < len(doc7.records) and doc7.records[end]['tag'] == 0:
                        end += 1
                    break
            name_stories.append((start, end, i, txt))
        elif 'Mandiri Call 14000' in txt:
            end = None
            for k in range(i, min(len(doc7.records), i+15)):
                if doc7.records[k]['tag'] == 2203:
                    end = k + 1
                    while end < len(doc7.records) and doc7.records[end]['tag'] == 0:
                        end += 1
                    break
            mandiris.append((i, end, txt))

print(f"Found {len(name_stories)} Name stories:")
for idx, (s, e, r_i, txt) in enumerate(name_stories, 1):
    print(f"  Page {idx}: Start={s}, End={e}, TextRec={r_i} ({txt!r})")

print(f"\nFound {len(mandiris)} Mandiri Call objects:")
for idx, (r_i, e, txt) in enumerate(mandiris, 1):
    print(f"  Page {idx}: TextRec={r_i}, End={e}")
