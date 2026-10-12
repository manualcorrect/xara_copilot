import os, sys, struct
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from xar_dom_engine import XarDocument

xar_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\0.xar'
doc = XarDocument(xar_path)
spreads = [i for i, r in enumerate(doc.records) if r['tag'] == 46]

stories = []
for i, rec in enumerate(doc.records):
    if rec['tag'] == 2100 and rec['size'] >= 8:
        x, y = struct.unpack('<ii', rec['payload'][:8])
        page = sum(1 for sp in spreads if i >= sp) + 1
        texts = []
        for j in range(i + 1, min(len(doc.records), i + 35)):
            if doc.records[j]['tag'] == 2100:
                break
            if doc.records[j]['tag'] in (2201, 2202):
                t = doc.records[j]['payload'].decode('utf-16le', errors='ignore').strip('\x00')
                if t:
                    texts.append((j, doc.records[j]['tag'], t))
        if texts:
            stories.append({'idx': i, 'page': page, 'x': x, 'y': y, 'texts': texts, 'full_text': ''.join(t[2] for t in texts)})

for p in range(1, 6):
    print(f"\nPage {p} Page Number stories:")
    for s in stories:
        if s['page'] == p and ('of' in s['full_text'].lower() or 'dari' in s['full_text'].lower()):
            print(f"  idx={s['idx']} x={s['x']} y={s['y']} -> {repr(s['full_text'])}")
            for t in s['texts']:
                print(f"    rec {t[0]} tag {t[1]} ({doc.records[t[0]]['size']}b): {repr(t[2])}")



# Check table saldo rows
saldo_stories_table = []
for s in stories:
    is_table_y = (s['y'] <= 520000) if s['page'] == 1 else (s['y'] <= 660000)
    if 470000 <= s['x'] <= 575000 and is_table_y and s['y'] >= 40000:
        if ',' in s['full_text'] or '.' in s['full_text']:
            saldo_stories_table.append(s)

saldo_stories_table.sort(key=lambda s: (s['page'], -s['y']))
print(f"\nTotal table saldo rows detected: {len(saldo_stories_table)}")

from run_project_v2_pipeline import calc_text_width

nom_xrs = []
saldo_xrs = []
for r_idx, s_story in enumerate(saldo_stories_table):
    p_num = s_story['page']
    row_y = s_story['y']
    row_stories = [s for s in stories if s['page'] == p_num and abs(s['y'] - row_y) <= 12000]
    nom_story = [s for s in row_stories if 300000 <= s['x'] <= 460000]
    
    # Saldo
    w_s = calc_text_width(s_story['full_text'].strip())
    xr_s = s_story['x'] + w_s
    saldo_xrs.append(xr_s)
    
    # Nominal
    if nom_story:
        w_n = calc_text_width(nom_story[0]['full_text'].strip())
        xr_n = nom_story[0]['x'] + w_n
        nom_xrs.append(xr_n)

print(f"Native Saldo XR: min={min(saldo_xrs)}, max={max(saldo_xrs)}, avg={sum(saldo_xrs)/len(saldo_xrs):.1f}")
if nom_xrs:
    print(f"Native Nom XR:   min={min(nom_xrs)}, max={max(nom_xrs)}, avg={sum(nom_xrs)/len(nom_xrs):.1f}")


for r_idx in range(5):
    s_story = saldo_stories_table[r_idx]
    p_num = s_story['page']
    row_y = s_story['y']
    row_stories = [s for s in stories if s['page'] == p_num and abs(s['y'] - row_y) <= 12000]
    dt_stories = [s for s in row_stories if 50000 <= s['x'] <= 95000]
    print(f"\nRow {r_idx+1} Date/Time stories (count={len(dt_stories)}):")
    for s in dt_stories:
        print(f"  idx={s['idx']} x={s['x']} y={s['y']} -> {repr(s['full_text'])}")
        for t in s['texts']:
            print(f"    rec {t[0]} tag {t[1]} ({doc.records[t[0]]['size']}b): {repr(t[2])}")








