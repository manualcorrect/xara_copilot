import os
import json
import openpyxl
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

aug_dir = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug"
xar_path = os.path.join(aug_dir, "0.xar")
xlsx_path = os.path.join(aug_dir, "Template_Pekerjaan_Xara_Aug.xlsx")

print("=== INSPECTING AUG INPUTS ===")
doc = XarDocument(xar_path)
print(f"Loaded 0.xar: {len(doc.records):,} records.")

wb = openpyxl.load_workbook(xlsx_path, data_only=True)
print("Sheet names:", wb.sheetnames)

# Inspect Header & Ringkasan
ws_h = wb['Header & Ringkasan']
print("\n--- Header & Ringkasan ---")
for r in range(1, 26):
    row_vals = [ws_h.cell(r, c).value for c in range(1, 6)]
    if any(v is not None for v in row_vals):
        print(f"Row {r:02d}: {row_vals}")

# Inspect Tabel_Mutasi
ws_m = wb['Tabel_Mutasi']
print("\n--- Tabel_Mutasi (First 40 rows) ---")
mutasi_rows = []
for r in range(4, 50):
    row_vals = [ws_m.cell(r, c).value for c in range(1, 11)]
    if any(v is not None for v in row_vals):
        print(f"Row {r:02d}: {row_vals}")
        mutasi_rows.append(row_vals)

print(f"\nTotal transaction rows in Excel: {len([r for r in mutasi_rows[1:] if r[0] not in ('[AWAL]', None)])}")
