import sys
import json
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

sys.stdout.reconfigure(encoding='utf-8')

aug_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Aug"
xar_path = f"{aug_dir}\\0.xar"
excel_path = f"{aug_dir}\\Template_Pekerjaan_Xara_Aug.xlsx"

doc = XarDocument(xar_path)
cfg = parse_xara_excel_template(excel_path)

print(f"Total Records: {len(doc.records)}")
print("Excel Header:", cfg['header'])
print("Excel Summary:", cfg['summary'])
print("Excel Transactions Count:", len(cfg['transactions']))

# Print first few transactions
for i, tx in enumerate(cfg['transactions'][:10], 1):
    print(f"  Tx {i:2d}: Date={tx.get('tgl')} Time={tx.get('jam')} Desc={repr(tx.get('uraian'))} Nom={tx.get('nominal')} ({tx.get('tipe')}) Saldo={tx.get('saldo')}")

if len(cfg['transactions']) > 10:
    print(f"  ... ({len(cfg['transactions']) - 10} more)")
    for i, tx in enumerate(cfg['transactions'][10:], 11):
        print(f"  Tx {i:2d}: Date={tx.get('tgl')} Time={tx.get('jam')} Desc={repr(tx.get('uraian'))} Nom={tx.get('nominal')} ({tx.get('tipe')}) Saldo={tx.get('saldo')}")
