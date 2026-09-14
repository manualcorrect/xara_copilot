import os
import struct
import json
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print(f"Total records in aug/0.xar: {len(doc.records)}")

# 1. Check all pages (Pages are separated by Tag 29 or Tag 5000 or similar, or let's count pages)
# In Xara, each page has headers and table records.
# Let's find all Period strings, Dicetak strings, Halaman/Page strings, Name stories, Mandiri Call positions.

periods = []
dicetaks = []
halamans = []
rekenings = []
summaries = []
name_stories = []
mandiris = []

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        
        # Period
        if any(m in txt for m in ['01 Aug', '31 Aug', '01 Jul', '31 Jul', '01 Feb', '28 Feb', '29 Feb', '01 Jan', '31 Jan', '2026']):
            # check if it's period header (near 'Periode' or in header area)
            if '-' in txt and ('Aug' in txt or 'Jul' in txt or 'Feb' in txt or 'Jan' in txt):
                periods.append((i, r['tag'], txt))
                
        # Dicetak
        if txt.strip() in ['1', '0', '01', '10', 'Sep 2026', 'Aug 2026', 'Jul 2026', 'Feb 2026', 'Mar 2026']:
            # check context
            for k in range(max(0, i-10), i):
                if doc.records[k]['tag'] in (2201, 2202):
                    ptxt = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
                    if 'Dicetak' in ptxt or 'Printed' in ptxt or 'pada' in ptxt:
                        dicetaks.append((i, r['tag'], txt, ptxt))
                        break
                        
        # Halaman / Page
        if 'of' in txt or 'dari' in txt or txt.strip() in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            for k in range(max(0, i-8), min(len(doc.records), i+8)):
                if doc.records[k]['tag'] in (2201, 2202):
                    htxt = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
                    if 'Halaman' in htxt or 'Page' in htxt:
                        halamans.append((i, r['tag'], txt, htxt))
                        break

        # Rekening
        if any(txt.strip().startswith(prefix) for prefix in ['163', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '130', '131', '132', '133', '134', '135', '136', '137', '138', '139', '140', '141', '142', '143', '144', '145', '146', '147', '148', '149', '150']):
            if len(txt.strip()) >= 10:
                rekenings.append((i, r['tag'], txt))

print(f"Periods found: {len(periods)}")
for p in periods:
    print(f"  Period at {p[0]}: {p[2]!r}")

print(f"Rekening found: {len(rekenings)}")
for r in rekenings:
    print(f"  Rekening at {r[0]}: {r[2]!r}")

