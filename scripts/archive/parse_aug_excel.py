from parse_excel_template import parse_xara_excel_template

excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\Template_Pekerjaan_Xara_AUG.xlsx'
cfg = parse_xara_excel_template(excel_path)
print('Header:', cfg['header'])
print('Summary:', cfg['summary'])
print('Total transactions:', len(cfg['transactions']))
for tx in cfg['transactions']:
    print(f"  No {tx['no']:2d} (orig {tx['orig_no']:2d}): Tgl='{tx['tanggal']}' Jam='{tx['jam']}' Nom={tx['nominal']} Tipe={tx['tipe']} Saldo={tx['saldo']}")
