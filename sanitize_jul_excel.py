import openpyxl

excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\Template_Pekerjaan_Xara_JUL.xlsx'
wb = openpyxl.load_workbook(excel_path)

# 1. Sheet 1: Header & Ringkasan
ws1 = wb['Header & Ringkasan']
# Fix B7 output file
ws1['B7'] = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0_output.xar'

# Fix B23 Dana Keluar number format
cell_b23 = ws1['B23']
cell_b23.value = -5234704
cell_b23.number_format = '#,##0'

# 2. Sheet 2: Tabel_Mutasi
# Clean up Column B dates so they reflect July 2026 properly
ws2 = wb['Tabel_Mutasi']
ws2['B5'] = '01/07'

jul_dates_short = [
    '01/07', '01/07', '02/07', '02/07', '03/07',
    '04/07', '04/07', '05/07', '05/07', '06/07',
    '07/07', '07/07', '08/07', '09/07', '10/07',
    '11/07', '12/07', '13/07', '14/07', '14/07',
    '15/07', '15/07', '16/07', '31/07'
]

# Rows 6 to 29 in Excel
for idx, d_str in enumerate(jul_dates_short):
    row_num = 6 + idx
    ws2.cell(row=row_num, column=2).value = d_str

wb.save(excel_path)
print("Sanitization of Template_Pekerjaan_Xara_JUL.xlsx complete!")
