import os, sys, json, struct, openpyxl
from xar_dom_engine import XarDocument
from apply_flawless_roy_jun import CHAR_WIDTHS, calc_text_width, COLOR_GREEN, COLOR_BLACK, COLOR_BLUE, COLOR_GRAY, fmt_idr, update_text, blank_node, update_color, update_t2100_x, update_t2204, TARGET_XR_NOMINAL, extract_dom_rows

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jun'
in_path = os.path.join(folder, '0.xar')
excel_path = os.path.join(folder, 'Template_Pekerjaan_Xara_Jun.xlsx')

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws_hdr = wb['Header & Ringkasan']
ws_mut = wb['Tabel_Mutasi']

saldo_awal = float(ws_hdr.cell(21, 2).value or 2784795.81)
dana_masuk = float(ws_hdr.cell(22, 2).value or 10353000.0)
dana_keluar = float(ws_hdr.cell(23, 2).value or 13118126.0)
saldo_akhir = saldo_awal + dana_masuk - dana_keluar

excel_txs = []
for r in range(6, 88):
    nom = ws_mut.cell(r, 5).value
    bal = ws_mut.cell(r, 7).value
    excel_txs.append({
        'no': len(excel_txs) + 1,
        'nominal': float(nom),
        'saldo': float(bal)
    })

# Start from 0_tahap6.xar
doc = XarDocument(os.path.join(folder, '0_tahap6.xar'))
TOTAL_RECS = len(doc.records)

# Update Financial Summary Page 1 Header
str_awal = fmt_idr(saldo_awal) + " "
str_masuk_p1 = "+ " + fmt_idr(dana_masuk)[:-3]
str_masuk_p2 = fmt_idr(dana_masuk)[-3:]
str_keluar = "- " + fmt_idr(dana_keluar) + " "
str_akhir = fmt_idr(saldo_akhir)

update_text(doc, 1197, str_awal)
update_text(doc, 1207, str_masuk_p1)
update_text(doc, 1212, str_masuk_p2)
update_text(doc, 1226, str_keluar)
update_text(doc, 1239, str_akhir)

# Extract DOM rows
dom_rows = extract_dom_rows(doc)

for idx, (dom, tx) in enumerate(zip(dom_rows, excel_txs), 1):
    nom_val = tx['nominal']
    bal_val = tx['saldo']
    is_cr = (nom_val > 0)
    
    nom_sign = "+" if is_cr else "-"
    nom_str = nom_sign + fmt_idr(abs(nom_val))
    bal_str = fmt_idr(bal_val)
    
    # 1. Nominal
    update_text(doc, dom['n_rec'], nom_str)
    for s_idx in dom['n_splits']:
        blank_node(doc, s_idx)
    target_color = COLOR_GREEN if is_cr else COLOR_BLACK
    if dom['n_t150']:
        update_color(doc, dom['n_t150'], target_color)
    w_nom = calc_text_width(nom_str)
    new_nom_x = TARGET_XR_NOMINAL - w_nom
    if dom['n_t2100']:
        update_t2100_x(doc, dom['n_t2100'], new_nom_x)
        
    # 2. Saldo (Preserve base coordinate system with delta width adjustment)
    orig_bal_str = doc.records[dom['s_rec']]['payload'].decode('utf-16le', errors='ignore')
    w_orig_bal = calc_text_width(orig_bal_str)
    w_new_bal = calc_text_width(bal_str)
    delta_w = w_new_bal - w_orig_bal
    
    update_text(doc, dom['s_rec'], bal_str)
    for s_idx in dom['s_splits']:
        blank_node(doc, s_idx)
    if dom['s_t150']:
        update_color(doc, dom['s_t150'], COLOR_BLUE)
        
    if dom['s_t2204']:
        orig_dx, orig_dy = struct.unpack('<ii', doc.records[dom['s_t2204']]['payload'][:8])
        new_dx = orig_dx - delta_w
        update_t2204(doc, dom['s_t2204'], new_dx, orig_dy)

# Save
for r in doc.records:
    r['size'] = len(r['payload'])

doc.save(os.path.join(folder, '0_tahap7.xar'))
doc.save(os.path.join(folder, '0_output.xar'))
doc.save(os.path.join(folder, 'REK JUN_ROY_DARWIN.xar'))
print("[SUCCESS] 0_tahap7.xar, 0_output.xar, and REK JUN_ROY_DARWIN.xar fixed!")
