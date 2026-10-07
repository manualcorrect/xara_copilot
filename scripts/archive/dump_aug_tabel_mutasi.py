import openpyxl

excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\Template_Pekerjaan_Xara_Aug.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

print("=== ALL 110 ROWS IN TABEL_MUTASI ===")
for r in range(5, 116):
    no = ws.cell(r, 1).value
    tgl = ws.cell(r, 2).value
    jam = ws.cell(r, 3).value
    uraian = ws.cell(r, 4).value
    nom = ws.cell(r, 5).value
    tipe = ws.cell(r, 6).value
    saldo = ws.cell(r, 7).value
    print(f"Row {r:3d} | No: {str(no):>6s} | Tgl: {str(tgl):<25s} | Jam: {str(jam):<15s} | Nom: {str(nom):>15s} | Saldo: {str(saldo):>15s}")
