import json
import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar")

with open("aug_stories_extracted.json", "r", encoding="utf-8") as f:
    stories = json.load(f)

# Find all 34 nominal indices in stories
nom_indices = []
for i, s in enumerate(stories):
    txt = s['text'].strip()
    idx = s['idx']
    if (txt.startswith('+') or txt.startswith('-')) and any(c.isdigit() for c in txt) and ('WIB' not in txt) and ('Sep' not in txt):
        nom_indices.append(i)

print(f"Total nominal rows: {len(nom_indices)}")

rows_data = []
for row_num, nom_i in enumerate(nom_indices, 1):
    # Nominal node(s)
    st_nom = stories[nom_i]
    nom_nodes = [st_nom['idx']]
    # Check if next node is a split of nominal
    curr_i = nom_i + 1
    if curr_i < len(stories):
        next_t = stories[curr_i]['text'].strip()
        # If split is '00' or starts with '630' or fraction
        if (next_t == '00' or next_t.isdigit() or next_t.endswith(',00')) and ('WIB' not in next_t) and ('Sep' not in next_t):
            # Check if this could be the saldo
            # In Mandiri, saldo is positive and usually has comma like '74.803,00'
            if len(next_t) <= 4 or next_t in ('00', '630,00', '0,00'):
                nom_nodes.append(stories[curr_i]['idx'])
                curr_i += 1

    # Now Saldo nodes (after nominal, before Time)
    saldo_nodes = []
    while curr_i < len(stories):
        st_curr = stories[curr_i]
        txt = st_curr['text'].strip()
        if 'WIB' in txt or (':' in txt and any(c.isdigit() for c in txt)):
            # Found time
            break
        else:
            saldo_nodes.append(st_curr['idx'])
        curr_i += 1

    # Now Time nodes
    time_nodes = []
    while curr_i < len(stories):
        st_curr = stories[curr_i]
        txt = st_curr['text'].strip()
        time_nodes.append(st_curr['idx'])
        # Check if next node is time split or date
        if curr_i + 1 < len(stories):
            nxt = stories[curr_i + 1]['text'].strip()
            if nxt in ('WIB', 'IB', 'B') or ('WIB' in nxt and ':' not in nxt):
                time_nodes.append(stories[curr_i + 1]['idx'])
                curr_i += 1
        break

    # Now Date nodes
    date_nodes = []
    curr_i += 1
    while curr_i < len(stories):
        st_curr = stories[curr_i]
        txt = st_curr['text'].strip()
        date_nodes.append(st_curr['idx'])
        if 'Sep' in txt or '2025' in txt or '25' in txt:
            # Check if year is in next node
            if curr_i + 1 < len(stories) and stories[curr_i + 1]['text'].strip() in ('25', '2025'):
                date_nodes.append(stories[curr_i + 1]['idx'])
                curr_i += 1
            break
        curr_i += 1

    rows_data.append({
        "row_no": row_num,
        "nom_nodes": nom_nodes,
        "saldo_nodes": saldo_nodes,
        "time_nodes": time_nodes,
        "date_nodes": date_nodes
    })

for r in rows_data:
    nom_txt = "".join(doc.records[idx]['payload'].decode('utf-16le') for idx in r['nom_nodes'])
    saldo_txt = "".join(doc.records[idx]['payload'].decode('utf-16le') for idx in r['saldo_nodes'])
    time_txt = "".join(doc.records[idx]['payload'].decode('utf-16le') for idx in r['time_nodes'])
    date_txt = "".join(doc.records[idx]['payload'].decode('utf-16le') for idx in r['date_nodes'])
    print(f"Row {r['row_no']:02d}: Nom={repr(nom_txt):15s} | Saldo={repr(saldo_txt):15s} | Time={repr(time_txt):15s} | Date={repr(date_txt)}")

with open("aug_34_rows_detailed.json", "w", encoding="utf-8") as f:
    json.dump(rows_data, f, indent=2)
