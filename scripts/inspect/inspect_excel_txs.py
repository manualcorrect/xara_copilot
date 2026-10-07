import json
from parse_excel_template import parse_xara_excel_template

excel_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\Template_Pekerjaan_Xara_Jul.xlsx"
cfg = parse_xara_excel_template(excel_path)

print("=== EXCEL TRANSACTIONS ===")
for t in cfg['transactions']:
    print(f"Row {t['no']:02d}: Tanggal={repr(t['tanggal']):15s} | Jam={repr(t['jam']):15s} | Nom={repr(t['nominal']):15s} | Saldo={repr(t['saldo']):15s}")
