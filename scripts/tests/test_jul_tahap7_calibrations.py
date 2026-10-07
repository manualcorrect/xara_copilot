import json
import struct
from xar_dom_engine import XarDocument

with open('jul_final_tx_schedule.json', 'r', encoding='utf-8') as f:
    txs = json.load(f)

print("=" * 80)
print("TESTING TAG 2204 & NOMINAL CALIBRATIONS FOR 83 ROWS (JULY)")
print("=" * 80)

# In 0.xar, baseline saldo width in Tag 2204 dx:
# If original saldo was ~10 chars (e.g. 146.335,81), dx had baseline.
# Target saldo format is formatted as f"{saldo:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
# e.g. 1521347.81 -> "1.521.347,81" (12 chars: '1.', millions)
# If original was ~10 chars and new is 12 chars: delta dx = -610, dy = round(new_dx * 72)
# If original was ~9 chars (e.g. 21.347,81) and new is 12 chars: delta dx = -915
# If original was 12 chars and new is 12 chars: delta dx = 0

for tx in txs:
    s_val = tx["saldo"]
    s_str = f"{s_val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    tx["formatted_saldo"] = s_str
    
    orig_dx = tx["xar_row_info"]["orig_dx"]
    orig_s = tx["xar_row_info"]["orig_saldo"]
    
    # calculate delta
    delta_len = len(s_str) - len(orig_s)
    new_dx = orig_dx - (delta_len * 305)
    new_dy = round(new_dx * 72)
    
    tx["calibrated_dx"] = new_dx
    tx["calibrated_dy"] = new_dy
    
    # Nominal formatting
    nom_val = tx["nominal"]
    if nom_val > 0:
        nom_str = f"+{nom_val:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        nom_type = "CR"
    else:
        nom_str = f"-{abs(nom_val):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        nom_type = "DB"
    tx["formatted_nominal"] = nom_str
    tx["nom_type"] = nom_type

print(f"Calibrated 83 rows successfully!")
for tx in txs[:5]:
    print(f"Row {tx['index']:2d} | Saldo: '{tx['formatted_saldo']}' (dx={tx['calibrated_dx']}, dy={tx['calibrated_dy']}) | Nom: '{tx['formatted_nominal']}' [{tx['nom_type']}]")

for tx in txs[-5:]:
    print(f"Row {tx['index']:2d} | Saldo: '{tx['formatted_saldo']}' (dx={tx['calibrated_dx']}, dy={tx['calibrated_dy']}) | Nom: '{tx['formatted_nominal']}' [{tx['nom_type']}]")

with open('jul_final_tx_schedule.json', 'w', encoding='utf-8') as f:
    json.dump(txs, f, indent=2)
