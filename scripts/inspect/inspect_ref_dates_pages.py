import os
import sys
import struct

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from xar_dom_engine import XarDocument

p_ref = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\0.xar'
p_out = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\0_output.xar'

doc_ref = XarDocument(p_ref)
doc_out = XarDocument(p_out)
spreads = [i for i, r in enumerate(doc_ref.records) if r['tag'] == 46]

print("=== DETAIL HALAMAN 2: NOMOR HALAMAN DI REF ===")
# Inspect stories around y >= 700000 on Page 2 (records between spreads[1] and spreads[2])
sp1 = spreads[1]
sp2 = spreads[2]
for j in range(sp1, sp2):
    r = doc_ref.records[j]
    if r['tag'] == 2100 and r['size'] >= 8:
        x, y = struct.unpack('<ii', r['payload'][:8])
        if y >= 700000 and x >= 500000:
            print(f"Story {j} at x={x}, y={y}:")
            for k in range(j + 1, min(j + 30, sp2)):
                if doc_ref.records[k]['tag'] == 2100: break
                rf = doc_ref.records[k]
                ro = doc_out.records[k]
                if rf['tag'] in (2201, 2202):
                    t_ref = rf['payload'].decode('utf-16le', errors='ignore')
                    t_out = ro['payload'].decode('utf-16le', errors='ignore')
                    print(f"  rec {k} tag {rf['tag']}: REF={repr(t_ref)} | OUT={repr(t_out)}")

print("\n=== DETAIL TANGGAL & JAM TRANSAKSI DI REF (SEMUA BARIS) ===")
# Find all table rows by locating all table texts
rows = []
for i, r in enumerate(doc_ref.records):
    if r['tag'] == 2100 and r['size'] >= 8:
        x, y = struct.unpack('<ii', r['payload'][:8])
        page = sum(1 for sp in spreads if i >= sp) + 1
        is_table = (y <= 520000) if page == 1 else (y <= 660000)
        if is_table and y >= 40000:
            texts = []
            for k in range(i + 1, min(i + 20, len(doc_ref.records))):
                if doc_ref.records[k]['tag'] == 2100: break
                if doc_ref.records[k]['tag'] in (2201, 2202):
                    texts.append((k, doc_ref.records[k]['tag'], doc_ref.records[k]['payload'].decode('utf-16le', errors='ignore')))
            if texts:
                full_t = ''.join(t[2] for t in texts)
                rows.append({'idx': i, 'page': page, 'x': x, 'y': y, 'full_t': full_t, 'texts': texts})

# Group table rows by page and y (within 12000 mp)
# Find all saldos
saldos = [r for r in rows if 470000 <= r['x'] <= 575000 and (',' in r['full_t'] or '.' in r['full_t'])]
saldos.sort(key=lambda s: (s['page'], -s['y']))

print(f"Total saldos detected in REF: {len(saldos)}")
for idx, s in enumerate(saldos):
    p_num = s['page']
    row_y = s['y']
    # find all items in this row
    items_in_row = [r for r in rows if r['page'] == p_num and abs(r['y'] - row_y) <= 12000]
    dates = [r for r in items_in_row if 50000 <= r['x'] <= 95000]
    noms = [r for r in items_in_row if 300000 <= r['x'] <= 460000]
    
    date_strs_ref = [r['full_t'] for r in dates]
    
    # check OUT for the same date records
    date_strs_out = []
    for r in dates:
        t_out = ''
        for t_info in r['texts']:
            rec_k = t_info[0]
            t_out += doc_out.records[rec_k]['payload'].decode('utf-16le', errors='ignore')
        date_strs_out.append(t_out)
        
    print(f"Row {idx+1:02d} (P{p_num}, y={row_y}): REF Date/Time={date_strs_ref} | OUT Date/Time={date_strs_out}")
