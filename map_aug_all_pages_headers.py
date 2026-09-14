import os
import struct
import json
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== MAPPING ALL 10 PAGES HEADERS IN AUG/0.XAR ===")

pages = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'ROY DARWIN' in txt:
            # Found a page header name block
            pages.append(i)

print(f"Total pages detected by Name block: {len(pages)}")

all_page_maps = []
for p_idx, name_r_idx in enumerate(pages, 1):
    # Find Name story bounds
    story_start = None
    for k in range(max(0, name_r_idx-35), name_r_idx):
        if doc.records[k]['tag'] == 2100:
            story_start = k
    story_end = None
    for k in range(name_r_idx, min(len(doc.records), name_r_idx+25)):
        if doc.records[k]['tag'] == 2203:
            story_end = k
            while story_end+1 < len(doc.records) and doc.records[story_end+1]['tag'] == 0:
                story_end += 1
            break

    # Scan forward from story_end for Period, Dicetak, Page numbers
    scan_limit = min(len(doc.records), story_end + 350)
    
    # Period
    per_recs = []
    per_t2150 = None
    for k in range(story_end, scan_limit):
        if doc.records[k]['tag'] == 2150:
            per_t2150 = k
        if doc.records[k]['tag'] in (2201, 2202):
            txt = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
            if any(m in txt for m in ['Mar 202', 'Aug 202', 'Jul 202', 'Jan 202', 'Feb 202']) and '-' in txt:
                # Find all pieces of period
                for j in range(max(story_end, k-15), min(scan_limit, k+15)):
                    if doc.records[j]['tag'] in (2201, 2202):
                        ptxt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        per_recs.append((j, doc.records[j]['tag'], ptxt))
                break

    # Dicetak pada
    dicetak_recs = []
    for k in range(story_end, scan_limit):
        if doc.records[k]['tag'] in (2201, 2202):
            txt = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
            if 'Sep 2026' in txt or 'Aug 2026' in txt or 'Mar 2026' in txt:
                for j in range(max(story_end, k-12), min(scan_limit, k+5)):
                    if doc.records[j]['tag'] in (2201, 2202):
                        dtxt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        dicetak_recs.append((j, doc.records[j]['tag'], dtxt))
                break

    # Page number
    page_recs = []
    for k in range(story_end, scan_limit):
        if doc.records[k]['tag'] in (2201, 2202):
            txt = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
            if 'of ' in txt or 'dari ' in txt:
                for j in range(max(story_end, k-5), min(scan_limit, k+10)):
                    if doc.records[j]['tag'] in (2201, 2202):
                        pgtxt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        page_recs.append((j, doc.records[j]['tag'], pgtxt))
                break

    all_page_maps.append({
        'page': p_idx,
        'name_rec': name_r_idx,
        'story_start': story_start,
        'story_end': story_end,
        'per_t2150': per_t2150,
        'per_recs': per_recs,
        'dicetak_recs': dicetak_recs,
        'page_recs': page_recs
    })

print(json.dumps(all_page_maps, indent=2))
with open('aug_all_page_maps.json', 'w', encoding='utf-8') as f:
    json.dump(all_page_maps, f, indent=2)
