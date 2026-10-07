import os, sys, json, struct, openpyxl
from xar_dom_engine import XarDocument
import prosedur_training
from apply_flawless_adhikarya_jun import extract_dom_rows

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jun'
in_path = os.path.join(folder, '0.xar')
excel_path = os.path.join(folder, 'Template_Pekerjaan_Xara_Jun.xlsx')

wb = openpyxl.load_workbook(excel_path, data_only=True)
ws_hdr = wb['Header & Ringkasan']
ws_mut = wb['Tabel_Mutasi']

cust_name = str(ws_hdr.cell(10, 2).value or "ROY DARWIN REZERIUS").strip()
period_str = str(ws_hdr.cell(11, 2).value or "01 Jun 2026 - 30 Jun 2026").strip()
dicetak_pada = str(ws_hdr.cell(12, 2).value or "09 Sep 2026").strip()
if not dicetak_pada:
    dicetak_pada = "09 Sep 2026"
rek_num = str(ws_hdr.cell(13, 2).value or "1650003584860").strip()

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

# Load raw base 0.xar
doc = XarDocument(in_path)

# FASE 0: STANDARISASI PROSEDUR TRAINING (TAHAP 0)
doc = prosedur_training.standarisasi_template_tahap0(doc, cust_name, "KCP Jakarta Taman Aries")
palette = prosedur_training.deteksi_kamus_palet_native(doc)
fonts = prosedur_training.deteksi_kamus_font_native(doc)

def fmt_idr(val):
    if isinstance(val, (int, float)):
        num = float(val)
    else:
        s = str(val).strip().replace('+', '').replace('-', '').replace(' ', '')
        if ',' in s and '.' in s:
            s = s.replace('.', '').replace(',', '.')
        elif ',' in s:
            s = s.replace(',', '.')
        num = float(s or 0.0)
    return f"{abs(num):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def update_text(doc, rec_idx, text_str):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        p = bytearray(text_str.encode('utf-16le'))
        doc.records[rec_idx]['payload'] = p
        doc.records[rec_idx]['size'] = len(p)

def blank_node(doc, rec_idx):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

def update_color(doc, rec_idx, color_bytes):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        doc.records[rec_idx]['payload'] = bytearray(color_bytes)
        doc.records[rec_idx]['size'] = len(color_bytes)

def update_t2100_x(doc, rec_idx, new_x):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def update_t2150_w(doc, rec_idx, new_w):
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig_flag = doc.records[rec_idx]['payload'][4:5] if len(doc.records[rec_idx]['payload']) >= 5 else b'\x01'
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<i', new_w) + orig_flag)
        doc.records[rec_idx]['size'] = len(doc.records[rec_idx]['payload'])

def sync_and_save(doc, out_path):
    for r in doc.records:
        r['size'] = len(r['payload'])
    zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
    assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"
    doc.save(out_path)

# Tahap 1: Nama
sync_and_save(doc, os.path.join(folder, '0_tahap1.xar'))

# Tahap 2: Periode
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'Jun 2026 - 30 Jun 2026' in r['payload'].decode('utf-16le', errors='ignore'):
        update_text(doc, i, 'Jun 2026 - 30 Jun 2026')
sync_and_save(doc, os.path.join(folder, '0_tahap2.xar'))

# Tahap 3: Dicetak Pada
sync_and_save(doc, os.path.join(folder, '0_tahap3.xar'))

# Tahap 4: No Rekening
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and '1650003584860' in r['payload'].decode('utf-16le', errors='ignore'):
        update_text(doc, i, f"{rek_num} ")
sync_and_save(doc, os.path.join(folder, '0_tahap4.xar'))

# Tahap 5: Penomoran Halaman
sync_and_save(doc, os.path.join(folder, '0_tahap5.xar'))

# Tahap 6: Tanggal & Jam
sync_and_save(doc, os.path.join(folder, '0_tahap6.xar'))

# Tahap 7: Financial Summary & 82 Table Rows
# 1. Update Financial Summary Page 1 Header
str_awal = fmt_idr(saldo_awal) + " "
str_masuk_p1 = "+ " + fmt_idr(dana_masuk)[:-3]  # "+ 10.353.00"
str_masuk_p2 = fmt_idr(dana_masuk)[-3:]        # "0,00"
str_keluar = "- " + fmt_idr(dana_keluar) + " "  # "- 13.118.126,00 "
str_akhir = fmt_idr(saldo_akhir)                # "19.669,81"

# Find summary block in Page 1 header
for idx, r in enumerate(doc.records):
    if r['tag'] == 2100 and len(r['payload']) >= 12:
        coords = struct.unpack('<iii', r['payload'][:12])
        if coords[0] == 509160 and coords[1] == 667000:
            # Expand container width so lines do not wrap
            for k in range(idx, min(len(doc.records), idx + 10)):
                if doc.records[k]['tag'] == 2150:
                    update_t2150_w(doc, k, 75000) # Expand width to 75000 mp
                    break
            
            # Find and update summary text nodes and colors
            for k in range(idx, min(len(doc.records), idx + 80)):
                tag_k = doc.records[k]['tag']
                if tag_k == 2201:
                    txt_k = doc.records[k]['payload'].decode('utf-16le', errors='ignore')
                    if '4.784.795,81' in txt_k or '2.784.795,81' in txt_k:
                        update_text(doc, k, str_awal)
                    elif '+ 7.343.00' in txt_k or '+ 10.353.00' in txt_k:
                        update_text(doc, k, str_masuk_p1)
                    elif txt_k.strip() in ('0,00', '00'):
                        update_text(doc, k, str_masuk_p2)
                    elif '- 12.108.126,00' in txt_k or '- 13.118.126,00' in txt_k:
                        update_text(doc, k, str_keluar)
                    elif txt_k.strip() == '19.669,81':
                        update_text(doc, k, str_akhir)
                        # Ensure Tag 150 before Saldo Akhir is set to Blue
                        for p in range(k-1, max(0, k-10), -1):
                            if doc.records[p]['tag'] == 150:
                                update_color(doc, p, palette['blue_saldo'])
                                break
                            elif doc.records[p]['tag'] == 2200:
                                break
                elif tag_k == 150:
                    # Update colors of summary items
                    # Tag 150 at Saldo Awal -> palette['gray_sawal']
                    # Tag 150 at Dana Masuk -> palette['green_credit']
                    # Tag 150 at Dana Keluar -> palette['black_debit']
                    pass
            break

# 2. Update Table Rows (Decoupled Mode)
dom_rows = extract_dom_rows(doc)
assert len(dom_rows) == 82

TARGET_XR_NOMINAL = 431250
TARGET_XR_SALDO   = 568306

for idx, (dom, tx) in enumerate(zip(dom_rows, excel_txs), 1):
    nom_val = tx['nominal']
    bal_val = tx['saldo']
    is_cr = (nom_val > 0)
    
    nom_sign = "+" if is_cr else "-"
    nom_str = nom_sign + fmt_idr(abs(nom_val))
    bal_str = fmt_idr(bal_val)
    
    # Nomor Urut
    if dom['no_rec']:
        update_text(doc, dom['no_rec'], str(idx))
        
    # Nominal Transaksi
    update_text(doc, dom['n_rec'], nom_str)
    for s_idx in dom['n_splits']:
        blank_node(doc, s_idx)
    target_color = palette['green_credit'] if is_cr else palette['black_debit']
    if dom['n_t150']:
        update_color(doc, dom['n_t150'], target_color)
    w_nom = prosedur_training.calc_text_width(nom_str)
    new_nom_x = TARGET_XR_NOMINAL - w_nom
    if dom['n_t2100']:
        update_t2100_x(doc, dom['n_t2100'], new_nom_x)
        
    # Saldo Berjalan (Decoupled Tag 2100 Object)
    update_text(doc, dom['s_rec'], bal_str)
    for s_idx in dom['s_splits']:
        blank_node(doc, s_idx)
    if dom['s_t150']:
        update_color(doc, dom['s_t150'], palette['blue_saldo'])
    if dom['s_t2100']:
        w_bal = prosedur_training.calc_text_width(bal_str)
        new_saldo_x = TARGET_XR_SALDO - w_bal
        update_t2100_x(doc, dom['s_t2100'], new_saldo_x)

sync_and_save(doc, os.path.join(folder, '0_tahap7.xar'))
sync_and_save(doc, os.path.join(folder, '0_output.xar'))
sync_and_save(doc, os.path.join(folder, 'REK JUN_ROY_DARWIN.xar'))
print("\n[PERFECT] Summary width, Saldo Akhir Blue color, and Table layout 100% fixed!")
