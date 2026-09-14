import os
import struct
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== PAGE NUMBERING CONTEXT SCAN ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'of' in txt or 'dari' in txt:
            context = []
            for k in range(max(0, i-6), min(len(doc.records), i+8)):
                if doc.records[k]['tag'] in (2201, 2202):
                    context.append((k, doc.records[k]['tag'], doc.records[k]['payload'].decode('utf-16le', errors='ignore')))
            print(f"Page match at {i} ({txt!r}):")
            for c in context:
                print(f"   rec {c[0]} Tag {c[1]}: {c[2]!r}")
