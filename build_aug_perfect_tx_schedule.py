import json
import random
from xar_dom_engine import XarDocument

# Load parsed transactions and rows map
with open('aug_parsed_tx.json', 'r', encoding='utf-8') as f:
    tx_list = json.load(f)

with open('aug_rows_map.json', 'r', encoding='utf-8') as f:
    rows_map = json.load(f)

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

# Extract original date strings from 0.xar for each row
tx_dates_0xar = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Mar 2026' in txt and '-' not in txt:
            tx_dates_0xar.append((i, txt))

assert len(tx_dates_0xar) == 110, f"Expected 110 dates in 0.xar, got {len(tx_dates_0xar)}"

# Map resolved date from DD Mar 2026 to DD Aug 2026
for idx in range(110):
    rec_i, orig_d_txt = tx_dates_0xar[idx]
    day = orig_d_txt.split()[0]
    aug_date = f"{day} Aug 2026"
    tx_list[idx]["resolved_date"] = aug_date
    rows_map[idx]["date_prim"] = rec_i

# Generate deterministic ascending timestamps per day
random.seed(20260813)
date_groups = {}
for tx in tx_list:
    d = tx["resolved_date"]
    if d not in date_groups:
        date_groups[d] = []
    date_groups[d].append(tx)

for d, group in date_groups.items():
    n_tx = len(group)
    start_sec = 6 * 3600 + 15 * 60 # 06:15:00
    end_sec = 22 * 3600 + 45 * 60   # 22:45:00
    
    raw_secs = sorted(random.sample(range(start_sec, end_sec), n_tx))
    for i, tx in enumerate(group):
        if tx["row_idx"] == 110:
            tx["final_time"] = "23:59:00 WIB"
        else:
            sec = raw_secs[i]
            hh = sec // 3600
            mm = (sec % 3600) // 60
            ss = sec % 60
            tx["final_time"] = f"{hh:02d}:{mm:02d}:{ss:02d} WIB"

for i in range(110):
    tx_list[i]["row_info"] = rows_map[i]

with open('aug_final_tx_schedule.json', 'w', encoding='utf-8') as f:
    json.dump(tx_list, f, indent=2)

with open('aug_rows_map.json', 'w', encoding='utf-8') as f:
    json.dump(rows_map, f, indent=2)

print(f"[*] Successfully scheduled 110 transactions across {len(date_groups)} dates!")
print("\n--- SAMPLE ROWS ---")
for t in tx_list[:5]:
    print(f"Row {t['row_idx']:3d} | Date: {t['resolved_date']} | Time: {t['final_time']} | Nom: {t['formatted_nominal']:>16s} | Saldo: {t['formatted_saldo']:>16s}")
print("...")
for t in tx_list[-5:]:
    print(f"Row {t['row_idx']:3d} | Date: {t['resolved_date']} | Time: {t['final_time']} | Nom: {t['formatted_nominal']:>16s} | Saldo: {t['formatted_saldo']:>16s}")
