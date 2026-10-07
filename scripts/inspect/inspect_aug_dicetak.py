import os
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== DICETAK PADA CONTEXT ACROSS ALL 10 PAGES ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Sep 2026' in txt or 'Aug 2026' in txt or 'Mar 2026' in txt:
            # check if it has day before it
            prev_nodes = []
            for k in range(max(0, i-15), i):
                if doc.records[k]['tag'] in (2201, 2202):
                    prev_nodes.append((k, doc.records[k]['tag'], doc.records[k]['payload'].decode('utf-16le', errors='ignore')))
            print(f"Dicetak match at {i} ({txt!r}):")
            for pn in prev_nodes[-4:]:
                print(f"   prev {pn[0]} Tag {pn[1]}: {pn[2]!r}")
