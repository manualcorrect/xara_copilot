import sys
import json
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

sys.stdout.reconfigure(encoding='utf-8')

sep_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Sep"
xar_path = f"{sep_dir}\\0.xar"
excel_path = f"{sep_dir}\\Template_Pekerjaan_Xara_Sep.xlsx"

doc = XarDocument(xar_path)
cfg = parse_xara_excel_template(excel_path)

print(f"Total Records: {len(doc.records)}")
print("Excel Header:", cfg['header'])
print("Excel Summary:", cfg['summary'])
print("Excel Transactions Count:", len(cfg['transactions']))

# Print transactions
for i, tx in enumerate(cfg['transactions'], 1):
    print(f"  Tx {i:2d}: Date={tx.get('tgl')} Time={tx.get('jam')} Desc={repr(tx.get('uraian'))} Nom={tx.get('nominal')} ({tx.get('tipe')}) Saldo={tx.get('saldo')}")
