import json
import re

with open("extracted_all_stories.json", "r", encoding="utf-8") as f:
    stories = json.load(f)

# Let's inspect the flow
# Let's filter out headers and footer texts that are not row data
# Page 2 Header: Rec 3363 - 3888
# Page 3 Header: Rec 6225 - 6750

rows = []
i = 0
n = len(stories)

while i < n:
    st = stories[i]
    txt = st['text'].strip()
    idx = st['idx']

    # Skip headers
    if idx in range(3360, 3900) or idx in range(6220, 6760):
        i += 1
        continue

    # Look for Row Number: 1..34
    # Check if this node or combination is a row number
    # Notice row numbers can be 1-digit or 2-digit: '1', '2', ..., '10', '11' (one node or two nodes '1','0')
    if txt.isdigit() and 1 <= int(txt) <= 34 and len(rows) + 1 == int(txt):
        expected_row = len(rows) + 1
        row_no_idx = [idx]
        row_data = {"row_no": expected_row, "row_no_nodes": row_no_idx}
        
        # Now search forward for Nominal, Saldo, Time, Date
        # Find next nominal (+ or -)
        j = i + 1
        # Description nodes are between row_no and nominal
        desc_nodes = []
        nom_nodes = []
        saldo_nodes = []
        time_nodes = []
        date_nodes = []

        # Find nominal node
        while j < n:
            st_j = stories[j]
            t_j = st_j['text'].strip()
            # If t_j is nominal (+..., -..., or split '-' / '+')
            if (t_j.startswith('+') or t_j.startswith('-')) and any(c.isdigit() for c in t_j):
                nom_nodes.append(st_j['idx'])
                # Check if next node is fractional split of nominal (e.g. '00' or '99,00')
                if j + 1 < n:
                    next_t = stories[j+1]['text'].strip()
                    if (next_t.endswith(',00') or next_t == '00' or next_t.isdigit()) and ('WIB' not in next_t) and ('Sep' not in next_t) and ('202' not in next_t):
                        # But wait, make sure it's not the saldo node!
                        # If next_t has a comma like '99,00' or '00', it might be split
                        if len(next_t) <= 5 and (',' in next_t or next_t.isdigit()):
                            nom_nodes.append(stories[j+1]['idx'])
                            j += 1
                break
            elif t_j in ('-', '+') and j + 1 < n and any(c.isdigit() for c in stories[j+1]['text']):
                nom_nodes.append(st_j['idx'])
                nom_nodes.append(stories[j+1]['idx'])
                j += 1
                # check if there is a 3rd split
                if j + 1 < n and stories[j+1]['text'].strip().endswith(',00'):
                    nom_nodes.append(stories[j+1]['idx'])
                    j += 1
                break
            else:
                desc_nodes.append(st_j['idx'])
            j += 1

        # Now find Saldo nodes (after nominal, before Time)
        j += 1
        while j < n:
            st_j = stories[j]
            t_j = st_j['text'].strip()
            if 'WIB' in t_j or (':' in t_j and any(c.isdigit() for c in t_j)):
                # This is time!
                time_nodes.append(st_j['idx'])
                # Check if next node is split of time (e.g. 'WIB' or 'B')
                if j + 1 < n and ('WIB' in stories[j+1]['text'] or stories[j+1]['text'].strip() in ('WIB', 'IB', 'B')):
                    time_nodes.append(stories[j+1]['idx'])
                    j += 1
                break
            else:
                saldo_nodes.append(st_j['idx'])
            j += 1

        # Now find Date nodes (after Time)
        j += 1
        while j < n:
            st_j = stories[j]
            t_j = st_j['text'].strip()
            # Date contains 'Sep' or month or year '25' / '2025'
            date_nodes.append(st_j['idx'])
            if '25' in t_j or '2025' in t_j or '2026' in t_j:
                break
            if len(date_nodes) >= 2:
                break
            j += 1

        row_data['desc_nodes'] = desc_nodes
        row_data['nom_nodes'] = nom_nodes
        row_data['saldo_nodes'] = saldo_nodes
        row_data['time_nodes'] = time_nodes
        row_data['date_nodes'] = date_nodes

        rows.append(row_data)
        i = j
    else:
        # Check if 2-digit row number like '1' followed by '0'
        if txt.isdigit() and i + 1 < n and stories[i+1]['text'].strip().isdigit():
            combo = txt + stories[i+1]['text'].strip()
            if combo.isdigit() and int(combo) == len(rows) + 1:
                expected_row = len(rows) + 1
                row_no_idx = [idx, stories[i+1]['idx']]
                row_data = {"row_no": expected_row, "row_no_nodes": row_no_idx}
                # Repeat same logic
                j = i + 2
                desc_nodes = []
                nom_nodes = []
                saldo_nodes = []
                time_nodes = []
                date_nodes = []

                while j < n:
                    st_j = stories[j]
                    t_j = st_j['text'].strip()
                    if (t_j.startswith('+') or t_j.startswith('-')) and any(c.isdigit() for c in t_j):
                        nom_nodes.append(st_j['idx'])
                        if j + 1 < n:
                            next_t = stories[j+1]['text'].strip()
                            if (next_t.endswith(',00') or next_t == '00') and ('WIB' not in next_t):
                                nom_nodes.append(stories[j+1]['idx'])
                                j += 1
                        break
                    elif t_j in ('-', '+') and j + 1 < n and any(c.isdigit() for c in stories[j+1]['text']):
                        nom_nodes.append(st_j['idx'])
                        nom_nodes.append(stories[j+1]['idx'])
                        j += 1
                        break
                    else:
                        desc_nodes.append(st_j['idx'])
                    j += 1

                j += 1
                while j < n:
                    st_j = stories[j]
                    t_j = st_j['text'].strip()
                    if 'WIB' in t_j or (':' in t_j and any(c.isdigit() for c in t_j)):
                        time_nodes.append(st_j['idx'])
                        if j + 1 < n and ('WIB' in stories[j+1]['text'] or stories[j+1]['text'].strip() in ('WIB', 'IB', 'B')):
                            time_nodes.append(stories[j+1]['idx'])
                            j += 1
                        break
                    else:
                        saldo_nodes.append(st_j['idx'])
                    j += 1

                j += 1
                while j < n:
                    st_j = stories[j]
                    t_j = st_j['text'].strip()
                    date_nodes.append(st_j['idx'])
                    if '25' in t_j or '2025' in t_j or '2026' in t_j:
                        break
                    if len(date_nodes) >= 2:
                        break
                    j += 1

                row_data['desc_nodes'] = desc_nodes
                row_data['nom_nodes'] = nom_nodes
                row_data['saldo_nodes'] = saldo_nodes
                row_data['time_nodes'] = time_nodes
                row_data['date_nodes'] = date_nodes

                rows.append(row_data)
                i = j
        i += 1

print(f"Total rows parsed: {len(rows)}")
for r in rows:
    print(f"Row {r['row_no']:02d}: No={r['row_no_nodes']}, Nom={r['nom_nodes']}, Saldo={r['saldo_nodes']}, Time={r['time_nodes']}, Date={r['date_nodes']}")

with open("rows_34_map.json", "w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)
