from parse_excel_template import parse_xara_excel_template

excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\Template_Pekerjaan_Xara_JUL.xlsx'
cfg = parse_xara_excel_template(excel_path)
print("Project config:")
for k, v in cfg['project'].items():
    print(f"  {k}: {v}")

print("\nHeader config:")
for k, v in cfg['header'].items():
    print(f"  {k}: {v}")

print("\nSummary config:")
for k, v in cfg['summary'].items():
    print(f"  {k}: {v}")

print(f"\nTransactions count after normalization: {len(cfg['transactions'])}")
for r in cfg['transactions']:
    print(f"  No {r['no']}: Tgl={r['tgl']} Jam={r['jam']} Nom={r['nominal_raw']} ({r['tipe']}) Saldo={r['saldo_raw']}")
