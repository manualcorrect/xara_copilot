import openpyxl

excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\Template_Pekerjaan_Xara_Aug.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Header & Ringkasan']

print("=== HEADER & RINGKASAN SHEET CONTENT ===")
for r in range(1, 30):
    row_vals = [ws.cell(r, c).value for c in range(1, 10)]
    if any(v is not None for v in row_vals):
        print(f"Row {r:2d}: {row_vals}")
