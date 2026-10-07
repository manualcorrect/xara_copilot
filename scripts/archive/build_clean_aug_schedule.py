import os
import openpyxl
import json
import random
from datetime import datetime, time
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug'
excel_path = os.path.join(folder, 'Template_Pekerjaan_Xara_Aug.xlsx')
xar_path = os.path.join(folder, '0.xar')

doc = XarDocument(xar_path)
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws_mutasi = wb['Tabel_Mutasi']

# Load 0.xar dates
tx_dates_0xar = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Mar 2026' in txt and '-' not in txt:
            tx_dates_0xar.append((i, txt))

assert len(tx_dates_0xar) == 110, f"Expected 110 dates in 0.xar, got {len(tx_dates_0xar)}"

with open('aug_rows_map.json', 'r', encoding='utf-8') as f:
    rows_map = json.load(f)

# Extract and resolve all 110 transactions
tx_list = []
for r in range(6, 116):
    tx_idx = r - 5 # 1 to 110
    row_no = ws_mutasi.cell(r, 1).value
    tgl_val = ws_mutasi.cell(r, 2).value
    jam_val = ws_mutasi.cell(r, 3).value
    uraian_val = ws_mutasi.cell(r, 4).value
    nom_val = ws_mutasi.cell(r, 5).value
    tipe_val = ws_mutasi.cell(r, 6).value
    saldo_val = ws_mutasi.cell(r, 7).value
    
    nom_float = float(nom_val) if nom_val is not None else 0.0
    saldo_float = float(saldo_val) if saldo_val is not None else 0.0
    nom_type = "CR" if nom_float > 0 else "DB"
    
    # Format nominal: "+7.800.000,00" or "-107.000,00"
    abs_nom = abs(nom_float)
    int_part = int(abs_nom)
    dec_part = int(round((abs_nom - int_part) * 100))
    nom_str_formatted = f"{int_part:,}".replace(',', '.') + f",{dec_part:02d}"
    if nom_float > 0:
        formatted_nominal = f"+{nom_str_formatted}"
    else:
        formatted_nominal = f"-{nom_str_formatted}"
        
    # Format saldo: "7.930.488,81"
    s_int = int(saldo_float)
    s_dec = int(round((saldo_float - s_int) * 100))
    formatted_saldo = f"{s_int:,}".replace(',', '.') + f",{s_dec:02d}"
    
    # Resolve Date & Time
    # Check if explicit in Excel
    explicit_date = None
    explicit_time = None
    if isinstance(tgl_val, datetime):
        explicit_date = f"{tgl_val.day:02d} Aug 2026"
    elif isinstance(tgl_val, str) and '/' in tgl_val and not any(w in tgl_val for w in ['Users', 'BENDI', 'AUG', 'Rekening']):
        parts = tgl_val.strip().split('/')
        try:
            day = int(parts[0])
            explicit_date = f"{day:02d} Aug 2026"
        except:
            pass
            
    if isinstance(jam_val, time):
        explicit_time = f"{jam_val.strftime('%H:%M:%S')} WIB"
    elif isinstance(jam_val, str) and (':' in jam_val or 'WIB' in jam_val) and not any(w in jam_val for w in ['Users', 'BENDI', 'AUG', 'Rekening']):
        s = jam_val.strip()
        explicit_time = s if 'WIB' in s else f"{s} WIB"
        
    # Determine base date
    if tx_idx in (1, 2, 3):
        resolved_date = "01 Aug 2026"
    elif tx_idx in range(4, 9):
        resolved_date = "02 Aug 2026"
    elif tx_idx == 9:
        resolved_date = "05 Aug 2026"
    elif tx_idx == 10:
        resolved_date = "06 Aug 2026"
    elif tx_idx == 11:
        resolved_date = "08 Aug 2026"
    elif tx_idx in range(12, 23):
        resolved_date = "09 Aug 2026"
    elif tx_idx in range(96, 105): # Tx 96 to 104 -> 25 Aug 2026
        resolved_date = "25 Aug 2026"
    elif tx_idx in range(105, 111): # Tx 105 to 110 -> 31 Aug 2026
        resolved_date = "31 Aug 2026"
    elif explicit_date:
        resolved_date = explicit_date
    else:
        # Fallback to 0.xar day
        orig_day = tx_dates_0xar[tx_idx - 1][1].split()[0]
        resolved_date = f"{orig_day} Aug 2026"
        
    tx_list.append({
        'row_idx': tx_idx,
        'excel_row': r,
        'resolved_date': resolved_date,
        'explicit_time': explicit_time,
        'nom_float': nom_float,
        'nom_type': nom_type,
        'formatted_nominal': formatted_nominal,
        'saldo_float': saldo_float,
        'formatted_saldo': formatted_saldo,
        'uraian': str(uraian_val)
    })

# Smart ascending timestamps per date group
random.seed(20260825)
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
    
    # If group has Tx 96 (04:00:00 WIB), start earlier
    has_04 = any(t.get("explicit_time") == "04:00:00 WIB" for t in group)
    if has_04:
        start_sec = 4 * 3600 # 04:00:00
        
    raw_secs = sorted(random.sample(range(start_sec, end_sec), n_tx))
    for i, tx in enumerate(group):
        if tx.get("explicit_time"):
            tx["final_time"] = tx["explicit_time"]
        elif tx["row_idx"] == 110:
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

print(f"[*] Successfully scheduled all 110 transactions!")
print("\n--- SAMPLE CHECK TX 95 TO 100 ---")
for t in tx_list[94:102]:
    print(f"Row {t['row_idx']:3d} | Date: {t['resolved_date']} | Time: {t['final_time']} | Nom: {t['formatted_nominal']:>16s} ({t['nom_type']}) | Saldo: {t['formatted_saldo']:>16s}")
