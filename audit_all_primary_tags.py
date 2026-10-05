from xar_dom_engine import XarDocument
import json

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0_ORIGINAL_BACKUP.xar")
with open("perfect_34_rows_map.json", "r") as f:
    rows = json.load(f)

for r in rows:
    nom_tag = doc.records[r['nom_primary']]['tag']
    saldo_tag = doc.records[r['saldo_primary']]['tag']
    time_tag = doc.records[r['time_primary']]['tag']
    date_tag = doc.records[r['date_primary']]['tag']
    
    print(f"Row {r['row_no']:02d}: Nom_Rec {r['nom_primary']:5d} (Tag {nom_tag}), Saldo_Rec {r['saldo_primary']:5d} (Tag {saldo_tag}), Time_Rec {r['time_primary']:5d} (Tag {time_tag}), Date_Rec {r['date_primary']:5d} (Tag {date_tag})")
