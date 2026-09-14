import json
import random
from datetime import datetime, time

# Load parsed transactions and rows map
with open('aug_parsed_tx.json', 'r', encoding='utf-8') as f:
    tx_list = json.load(f)

with open('aug_rows_map.json', 'r', encoding='utf-8') as f:
    rows_map = json.load(f)

assert len(tx_list) == 110, f"Expected 110 transactions, got {len(tx_list)}"
assert len(rows_map) == 110, f"Expected 110 rows mapped, got {len(rows_map)}"

# Group transactions by resolved_date to generate realistic ascending timestamps
random.seed(202608) # Deterministic seed for August 2026
date_groups = {}
for tx in tx_list:
    d = tx["resolved_date"]
    if d not in date_groups:
        date_groups[d] = []
    date_groups[d].append(tx)

for d, group in date_groups.items():
    n_tx = len(group)
    start_sec = 6 * 3600 + 10 * 60 # 06:10:00
    end_sec = 22 * 3600 + 40 * 60   # 22:40:00
    
    # Generate n_tx strictly ascending random timestamps
    raw_secs = sorted(random.sample(range(start_sec, end_sec), n_tx))
    for i, tx in enumerate(group):
        raw_t = tx.get("raw_time", "")
        if raw_t and raw_t != "None":
            if 'WIB' in raw_t:
                tx["final_time"] = raw_t
            else:
                tx["final_time"] = f"{raw_t} WIB"
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

print(f"[*] Successfully scheduled {len(tx_list)} August transactions across {len(date_groups)} dates!")
print("\n--- SAMPLE SCHEDULED ROWS (FIRST 5 & LAST 5) ---")
for t in tx_list[:5]:
    print(f"Row {t['row_idx']:3d} | Date: {t['resolved_date']} | Time: {t['final_time']} | Nom: {t['formatted_nominal']:>16s} | Saldo: {t['formatted_saldo']:>16s}")
print("...")
for t in tx_list[-5:]:
    print(f"Row {t['row_idx']:3d} | Date: {t['resolved_date']} | Time: {t['final_time']} | Nom: {t['formatted_nominal']:>16s} | Saldo: {t['formatted_saldo']:>16s}")
