import os
import json
import struct
import shutil
from xar_dom_engine import XarDocument

with open("perfect_34_rows_map.json", "r", encoding="utf-8") as f:
    rows_map = json.load(f)

# Fix Row 2
rows_map[1]['nom_primary'] = 1614
rows_map[1]['nom_splits'] = [1609]
rows_map[1]['nom_tag2100'] = 1593
rows_map[1]['nom_tag150'] = 1598
rows_map[1]['nom_tag2206'] = 1608

# Fix Row 3
rows_map[2]['nom_primary'] = 1786
rows_map[2]['nom_splits'] = [1781]
rows_map[2]['nom_tag2100'] = 1765
rows_map[2]['nom_tag150'] = 1770
rows_map[2]['nom_tag2206'] = 1780

# Fix Row 25
rows_map[24]['saldo_primary'] = 7246
rows_map[24]['saldo_splits'] = [7241, 7251]
rows_map[24]['saldo_tag2100'] = 7225
rows_map[24]['saldo_tag150'] = 7230
rows_map[24]['saldo_tag2206'] = 7240

with open("perfect_34_rows_map.json", "w", encoding="utf-8") as f:
    json.dump(rows_map, f, indent=2)

print("Updated perfect_34_rows_map.json with Tag 2201 primary nodes for Rows 2, 3, 25.")
