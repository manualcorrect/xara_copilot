import openpyxl

wb = openpyxl.load_workbook(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\Template_Pekerjaan_Xara_Jul.xlsx", data_only=True)
ws = wb['Header & Ringkasan']

print("=== SHEET: Header & Ringkasan ===")
for r in range(1, 30):
    row_vals = [ws.cell(r, c).value for c in range(1, 10)]
    if any(v is not None for v in row_vals):
        print(f"Row {r:02d}: {row_vals}")
