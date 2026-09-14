import json
import struct
import openpyxl
from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUN\0.xar'
excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUN\Template_Pekerjaan_Xara_Jun.xlsx'

doc = XarDocument(xar_path)
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb['Tabel_Mutasi']

page_starts = [idx for idx, rec in enumerate(doc.records) if rec['tag'] == 2201 and 'Menara Mandiri' in rec['payload'].decode('utf-16le', errors='ignore')]
print(f"Total pages: {len(page_starts)}")

expected_rows_per_page = [10, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 5]

full_rows_map = {}
global_row = 1

for p_idx, start_rec in enumerate(page_starts):
    page_num = p_idx + 1
    end_rec = page_starts[p_idx + 1] if p_idx + 1 < len(page_starts) else len(doc.records)
    scan_start = start_rec + 1100 if p_idx == 0 else start_rec + 600
    
    # Let's collect all text stories in the table area
    stories = []
    curr_story = []
    for r in range(scan_start, end_rec):
        rec = doc.records[r]
        if rec['tag'] in [2201, 2202]:
            try:
                curr_story.append((r, rec['tag'], rec['size'], rec['payload'].decode('utf-16le', errors='ignore')))
            except: pass
        elif rec['tag'] == 2203 and curr_story:
            first_r = curr_story[0][0]
            last_r = curr_story[-1][0]
            # Attributes
            t150 = None
            t150_rec = None
            t2206_rec = None
            t2100_rec = None
            for back_r in range(max(scan_start, first_r - 35), first_r):
                if doc.records[back_r]['tag'] == 150:
                    t150 = bytes(doc.records[back_r]['payload']).hex()
                    t150_rec = back_r
                elif doc.records[back_r]['tag'] == 2206:
                    t2206_rec = back_r
            # Forward Tag 2100 search
            for fwd_r in range(last_r, min(end_rec, last_r + 20)):
                if doc.records[fwd_r]['tag'] == 2100:
                    t2100_rec = fwd_r
                    break
            stories.append({
                'first_rec': first_r,
                'last_rec': last_r,
                'recs': curr_story,
                'text': "".join(x[3] for x in curr_story),
                't150': t150,
                't150_rec': t150_rec,
                't2206_rec': t2206_rec,
                't2100_rec': t2100_rec
            })
            curr_story = []

    # Find Saldo stories on this page
    page_saldos = []
    for s in stories:
        st = s['text']
        if (st.endswith(',81') or st.endswith(',00') or st.endswith(',50')) and not st.startswith('+') and not st.startswith('-') and 'Tabungan' not in st and 'Mandiri' not in st and len(st) <= 25:
            page_saldos.append(s)
            
    print(f"Page {page_num:2d}: Found {len(page_saldos)} Saldos (Expected {expected_rows_per_page[p_idx]})")
    assert len(page_saldos) == expected_rows_per_page[p_idx], f"Page {page_num} Saldo count mismatch!"

    for s_in_page_idx, saldo_s in enumerate(page_saldos):
        # Find index of saldo_s in stories
        s_idx = stories.index(saldo_s)
        
        # Nominal story is usually s_idx + 1
        nominal_s = None
        for cand_idx in [s_idx + 1, s_idx + 2]:
            if cand_idx < len(stories) and (stories[cand_idx]['text'].startswith('+') or (stories[cand_idx]['text'].startswith('-') and len(stories[cand_idx]['text']) <= 20 and any(c.isdigit() for c in stories[cand_idx]['text']))):
                nominal_s = stories[cand_idx]
                break
        assert nominal_s is not None, f"Page {page_num} Row {s_in_page_idx+1} Nominal not found!"
        nom_idx = stories.index(nominal_s)
        
        # Time & Date stories:
        # On Page 1 Row 1: Time & Date are the very first stories on Page 1 table (before descriptions)
        # On all other rows: Time & Date are right after the nominal of the PREVIOUS row (or right before this row's description)
        # Or for the last row on a page, Time & Date might be right after this row's nominal!
        # Let's find Time & Date stories between previous row's nominal and this row's nominal
        time_s = None
        date_s = None
        
        if page_num == 1 and s_in_page_idx == 0:
            # Row 1: Time & Date are before Row 1 descriptions
            for s in stories[:s_idx]:
                if 'WIB' in s['text'] or 'WI' in s['text']:
                    time_s = s
                elif ('Apr 2026' in s['text'] or 'Apr 202' in s['text']) and '0 Apr' not in s['text']:
                    date_s = s
        else:
            # For row > 1 on page: look between previous row's nominal and current row's saldo
            prev_saldo_s = page_saldos[s_in_page_idx - 1]
            prev_nom_idx = stories.index(prev_saldo_s) + 1
            for s in stories[prev_nom_idx:s_idx]:
                if ('WIB' in s['text'] or 'WI' in s['text']) and time_s is None:
                    time_s = s
                elif (('Apr 2026' in s['text'] or 'Apr 202' in s['text']) and '0 Apr' not in s['text']) and date_s is None:
                    date_s = s
                    
            # If date_s or time_s is still None, look right after current row's nominal (e.g. for last row on page)
            if time_s is None:
                for s in stories[nom_idx+1:nom_idx+4]:
                    if 'WIB' in s['text'] or 'WI' in s['text']:
                        time_s = s
                        break
            if date_s is None:
                for s in stories[nom_idx+1:nom_idx+4]:
                    if ('Apr 2026' in s['text'] or 'Apr 202' in s['text']) and '0 Apr' not in s['text']:
                        date_s = s
                        break
                        
        row_entry = {
            'row_num': global_row,
            'page': page_num,
            's_txt': saldo_s['recs'][0][0],
            's_splits': [r[0] for r in saldo_s['recs'][1:]],
            's_orig_text': saldo_s['text'],
            's_2206': saldo_s['t2206_rec'],
            's_2100': saldo_s['t2100_rec'],
            
            'n_txt': nominal_s['recs'][0][0],
            'n_splits': [r[0] for r in nominal_s['recs'][1:]],
            'n_orig_text': nominal_s['text'],
            'n_150': nominal_s['t150_rec'],
            'n_2206': nominal_s['t2206_rec'],
            'n_2100': nominal_s['t2100_rec'],
            
            't_recs': [(r[0], r[3]) for r in time_s['recs']] if time_s else [],
            't_orig_text': time_s['text'] if time_s else '',
            'd_recs': [(r[0], r[3]) for r in date_s['recs']] if date_s else [],
            'd_orig_text': date_s['text'] if date_s else ''
        }
        full_rows_map[global_row] = row_entry
        global_row += 1

print(f"\nSuccessfully mapped {len(full_rows_map)} rows!")
with open('adhikarya_jun_rows_map.json', 'w', encoding='utf-8') as f:
    json.dump(full_rows_map, f, indent=2)

print("[OK] Saved to adhikarya_jun_rows_map.json")
