import os
import sys
import struct
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template
from smart_date_time_generator import generate_smart_schedule
from run_project_v2_pipeline import (
    calc_text_width, fmt_idr, update_text_node, clean_split_node,
    update_t2206, update_t2100, update_color
)

xlsx_path = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\Template_Pekerjaan_Xara_Jul.xlsx'
xar_in = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\0.xar'
xar_out = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\0_test_run.xar'

cfg = parse_xara_excel_template(xlsx_path)
doc = XarDocument(xar_in)
n_recs = len(doc.records)

def find_prec_tag(rec_idx, target_tag, min_size=0, search_back=40):
    for j in range(rec_idx - 1, max(0, rec_idx - search_back), -1):
        r = doc.records[j]
        if r['tag'] == target_tag and len(r['payload']) >= min_size:
            return j
    return None

def clean_trailing_split_nodes(start_idx, max_forward=30):
    for k in range(start_idx + 1, min(n_recs, start_idx + max_forward)):
        if doc.records[k]['tag'] in (2100, 2200, 2203):
            break
        if doc.records[k]['tag'] in (2201, 2202):
            doc.records[k]['payload'] = bytearray(b'\x00\x00')
            doc.records[k]['size'] = 2

# Native Colors
c_hijau = bytearray.fromhex('0a040000') # #00A651 / green
c_hitam = bytearray.fromhex('75020000') # black
c_saldo = bytearray.fromhex('87050000') # blue
c_sawal = bytearray.fromhex('85030000') # gray

# Spreads
spreads = [i for i, r in enumerate(doc.records) if r['tag'] == 46]
tot_pages = len(spreads)

# Extract stories
stories = []
for i, rec in enumerate(doc.records):
    if rec['tag'] == 2100 and rec['size'] >= 8:
        x, y = struct.unpack('<ii', rec['payload'][:8])
        page = sum(1 for sp in spreads if i >= sp) + 1
        texts = []
        for j in range(i + 1, min(n_recs, i + 250)):
            if doc.records[j]['tag'] == 2100:
                break
            if doc.records[j]['tag'] in (2201, 2202):
                t = doc.records[j]['payload'].decode('utf-16le', errors='ignore').strip('\x00')
                if t:
                    texts.append((j, doc.records[j]['tag'], t))
        if texts:
            stories.append({'idx': i, 'page': page, 'x': x, 'y': y, 'texts': texts, 'full_text': ''.join(t[2] for t in texts)})

print(f"Extracted {len(stories)} text stories across {tot_pages} pages")

# 1. Tahap 1: Nama Nasabah (ALL CAPS)
new_name = cfg['header']['nama'].strip().upper()
t1_count = 0
for s in stories:
    if s['y'] >= 700000 and 120000 <= s['x'] <= 130000:
        first_t = s['texts'][0][0]
        update_text_node(doc, first_t, new_name + " ")
        clean_trailing_split_nodes(first_t)
        t1_count += 1
print(f"Tahap 1 (Nama): {t1_count} headers updated to '{new_name}'")

# 2. Tahap 2 & 3: Periode & Dicetak Pada
new_per = cfg['header']['periode'].strip()
new_cetak = cfg['header']['dicetak_pada'].strip()
t2_count = 0
t3_count = 0

for s in stories:
    if s['y'] >= 700000 and 330000 <= s['x'] <= 350000:
        # Check lines inside story
        lines_text_recs = []
        curr_line = []
        for j in range(s['idx'], min(n_recs, s['idx'] + 100)):
            r = doc.records[j]
            if r['tag'] == 2203:
                if curr_line:
                    lines_text_recs.append(curr_line)
                    curr_line = []
            elif r['tag'] in (2201, 2202):
                curr_line.append(j)
            elif r['tag'] == 2100 and j > s['idx']:
                break
        if curr_line:
            lines_text_recs.append(curr_line)
        
        if len(lines_text_recs) >= 2:
            # Line 1: Periode
            line1_recs = lines_text_recs[0]
            update_text_node(doc, line1_recs[0], new_per)
            for rk in line1_recs[1:]:
                clean_split_node(doc, rk)
            t2_count += 1
            
            # Line 2: Dicetak Pada
            line2_recs = lines_text_recs[1]
            update_text_node(doc, line2_recs[0], new_cetak)
            for rk in line2_recs[1:]:
                clean_split_node(doc, rk)
            t3_count += 1

print(f"Tahap 2 (Periode): {t2_count} nodes updated to '{new_per}'")
print(f"Tahap 3 (Dicetak): {t3_count} nodes updated to '{new_cetak}'")

# 3. Tahap 4: Nomor Rekening
new_acc = cfg['header']['nomor_rekening'].strip() + " "
t4_count = 0
for s in stories:
    if s['page'] == 1 and 640000 <= s['y'] <= 660000 and 140000 <= s['x'] <= 160000:
        digit_recs = [t[0] for t in s['texts'] if any(c.isdigit() for c in t[2])]
        if digit_recs:
            update_text_node(doc, digit_recs[0], new_acc)
            for rk in digit_recs[1:]:
                clean_split_node(doc, rk)
            t4_count += 1
print(f"Tahap 4 (No. Rek): {t4_count} header updated to '{new_acc.strip()}'")

# 4. Tahap 5: Nomor Halaman Multi-Digit Bersih
for p in range(1, tot_pages + 1):
    str_en = f"{p} of {tot_pages}"
    str_id = f"{p} dari {tot_pages}"
    for s in stories:
        if s['page'] == p and s['y'] >= 700000 and s['x'] >= 500000:
            txt = s['full_text'].lower()
            if 'of' in txt:
                first_t = s['texts'][0][0]
                update_text_node(doc, first_t, str_en)
                clean_trailing_split_nodes(first_t)
            elif 'dari' in txt:
                first_t = s['texts'][0][0]
                update_text_node(doc, first_t, str_id)
                clean_trailing_split_nodes(first_t)
            elif txt == str(tot_pages) or txt == '5':
                # Split node with page count alone
                clean_split_node(doc, s['texts'][0][0])
print(f"Tahap 5 (Halaman): 1 of {tot_pages} s.d. {tot_pages} of {tot_pages} synchronized")

# 5. Tahap 7 Summary Header: Story 1247
sawal = cfg['summary']['saldo_awal']
dmasuk = cfg['summary']['dana_masuk']
dkeluar = cfg['summary']['dana_keluar']
sakhir = cfg['summary']['saldo_akhir']

val_masuk = dmasuk if dmasuk.startswith("+") else f"+ {dmasuk}"
val_keluar = dkeluar if dkeluar.startswith("-") else f"- {dkeluar}"

update_text_node(doc, 1266, sawal + " ")
clean_trailing_split_nodes(1266)
update_t2206(doc, 1261, calc_text_width(sawal))
update_color(doc, 1262, c_sawal)

update_text_node(doc, 1275, val_masuk + " ")
clean_trailing_split_nodes(1275)
clean_split_node(doc, 1280)
update_t2206(doc, 1270, calc_text_width(val_masuk))
update_color(doc, 1271, c_hijau)

update_text_node(doc, 1292, val_keluar + " ")
clean_trailing_split_nodes(1292)
update_t2206(doc, 1285, calc_text_width(val_keluar))
update_color(doc, 1286, c_hitam)

update_text_node(doc, 1304, sakhir + " ")
clean_trailing_split_nodes(1304)
update_t2206(doc, 1296, calc_text_width(sakhir))
update_color(doc, 1298, c_saldo)
print(f"Tahap 7 (Summary Header): Awal={sawal}, Masuk={val_masuk}, Keluar={val_keluar}, Akhir={sakhir}")

# 6. Tahap 6 & 7: 47 Table Rows
saldo_stories_table = []
for s in stories:
    is_table_y = (s['y'] <= 520000) if s['page'] == 1 else (s['y'] <= 660000)
    if 470000 <= s['x'] <= 575000 and is_table_y and s['y'] >= 40000:
        if ',' in s['full_text'] or '.' in s['full_text']:
            saldo_stories_table.append(s)

saldo_stories_table.sort(key=lambda s: (s['page'], -s['y']))
total_physical_rows = len(saldo_stories_table)
print(f"Total physical table rows detected: {total_physical_rows}")

# Generate smart schedule for empty dates
smart_sched = generate_smart_schedule(total_physical_rows, period_start="2026-07-01", period_end="2026-07-31")

tx_list = cfg.get('transactions', [])
n_process = min(total_physical_rows, len(tx_list))

TARGET_XR_NOMINAL = 431320
TARGET_XR_SALDO = 570450

for r_idx in range(n_process):
    tx = tx_list[r_idx]
    s_story = saldo_stories_table[r_idx]
    p_num = s_story['page']
    row_y = s_story['y']

    row_stories = [s for s in stories if s['page'] == p_num and abs(s['y'] - row_y) <= 12000]

    no_story = None
    dt_stories = []
    nom_story = None

    for s in row_stories:
        if s['x'] <= 35000:
            no_story = s
        elif 50000 <= s['x'] <= 95000:
            dt_stories.append(s)
        elif 300000 <= s['x'] <= 460000:
            nom_story = s

    # 1. Update Nomor Urut
    if no_story and len(no_story['texts']) > 0:
        target_no = str(r_idx + 1)
        first_t = no_story['texts'][0][0]
        if len(no_story['texts']) >= 2 and len(target_no) >= 2:
            doc.records[no_story['texts'][0][0]]['payload'] = bytearray(target_no[0].encode('utf-16le'))
            doc.records[no_story['texts'][0][0]]['size'] = 2
            doc.records[no_story['texts'][1][0]]['payload'] = bytearray(target_no[1].encode('utf-16le'))
            doc.records[no_story['texts'][1][0]]['size'] = 2
        else:
            update_text_node(doc, first_t, target_no)
            clean_trailing_split_nodes(first_t)

    # 2. Update Tanggal & Jam (Tahap 6)
    tgl_val = tx.get('tanggal') or smart_sched[r_idx]['date_full']
    jam_val = tx.get('jam') or smart_sched[r_idx]['time']

    if dt_stories:
        for s in dt_stories:
            t_txt = s['full_text']
            first_t = s['texts'][0][0]
            if 'WIB' in t_txt or ':' in t_txt:
                update_text_node(doc, first_t, jam_val)
                clean_trailing_split_nodes(first_t)
            else:
                update_text_node(doc, first_t, tgl_val)
                clean_trailing_split_nodes(first_t)

    # 3. Update Nominal & Rata Kanan (Tahap 7)
    if nom_story and len(nom_story['texts']) > 0:
        nom_raw = str(tx.get('nominal', '')).strip()
        nom_fmt = fmt_idr(nom_raw)
        is_cr = not str(nom_raw).startswith('-')
        nom_final = f"+{nom_fmt}" if is_cr else f"-{nom_fmt}"

        rec_nom = nom_story['texts'][0][0]
        update_text_node(doc, rec_nom, nom_final)
        clean_trailing_split_nodes(rec_nom)

        nom_c = find_prec_tag(rec_nom, 150, 4)
        if nom_c:
            update_color(doc, nom_c, c_hijau if is_cr else c_hitam)

        nom_k = find_prec_tag(rec_nom, 2206, 12)
        nom_m = find_prec_tag(rec_nom, 2100, 12)
        w_nom = calc_text_width(nom_final)
        if nom_k: update_t2206(doc, nom_k, w_nom)
        if nom_m: update_t2100(doc, nom_m, TARGET_XR_NOMINAL - w_nom)

    # 4. Update Saldo & Rata Kanan (Tahap 7)
    rec_saldo = s_story['texts'][0][0]
    saldo_fmt = fmt_idr(tx.get('saldo', '0'))
    update_text_node(doc, rec_saldo, saldo_fmt)
    clean_trailing_split_nodes(rec_saldo)

    saldo_c = find_prec_tag(rec_saldo, 150, 4)
    if saldo_c:
        update_color(doc, saldo_c, c_saldo)

    saldo_k = find_prec_tag(rec_saldo, 2206, 12)
    saldo_m = find_prec_tag(rec_saldo, 2100, 12)
    w_saldo = calc_text_width(saldo_fmt)
    if saldo_k: update_t2206(doc, saldo_k, w_saldo)
    if saldo_m: update_t2100(doc, saldo_m, TARGET_XR_SALDO - w_saldo)

print(f"Tahap 6 & 7: {n_process} transaction rows updated successfully")

# Post-flight auto-sync & assertions
for r in doc.records:
    r['size'] = len(r['payload'])

assert len(doc.records) == n_recs, "Zero-shift invariant violated!"
zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
assert len(zero_nodes) == 0, f"Found 0-byte nodes: {zero_nodes}"

doc.save(xar_out)
print(f"SUCCESS: Saved test output to {xar_out} ({len(doc.records)} records)")
