import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Let's inspect the exact layout around each of the 22 rows
# We can search by nominal text:
nom_patterns = [
    # Page 1
    (1, '-397.5', 1587),
    (2, '-30.000,00', 1778),
    (3, '-42.000,00', 1949),
    (4, '-200.000,00', 2115),
    (5, '+15.200,00', 2316),
    (6, '-8.000,00', 2477),
    (7, '-18.000,00', 2643),
    (8, '+500.000,00', 2823),
    (9, '-500.704,', 3014),
    (10, '+80.000,00', 3192),
    # Page 2
    (11, '+500.000,00', 4215),
    (12, '-350.500,', 4401),
    (13, '-130.000,00', 4587),
    (14, '-45.000,00', 4753),
    (15, '+500.000,00', 4929),
    (16, '+50.000,00', 5114),
    (17, '-450.000,00', 5300),
    (18, '-50.000,00', 5471),
    (19, '-50.000,00', 5632),
    (20, '+488.000,00', 5808),
    (21, '-488.000,00', 5994),
    (22, '+500.000,00', 6160),
]

row_maps = {}

for row_num, pat, n_idx in nom_patterns:
    # 1. Nominal
    # Check text around n_idx
    n_rec = doc.records[n_idx]
    n_txt = n_rec['payload'].decode('utf-16le').rstrip('\x00')
    
    # Check if there is a split node after n_idx
    n_split = None
    next_rec = doc.records[n_idx + 5] if n_idx + 5 < len(doc.records) else None
    if next_rec and next_rec['tag'] in (2201, 2202):
        t_next = next_rec['payload'].decode('utf-16le').rstrip('\x00')
        if t_next in ('00', '00,00', ',00', '7,00'):
            n_split = n_idx + 5
            n_txt += t_next

    # Find Tag 2206, Tag 2100, Tag 150 for Nominal
    n_2206 = None
    n_2100 = None
    n_150 = None
    for j in range(n_idx - 15, n_idx):
        if doc.records[j]['tag'] == 2206 and n_2206 is None: n_2206 = j
        if doc.records[j]['tag'] == 150: n_150 = j
    for j in range(n_idx, n_idx + 15):
        if doc.records[j]['tag'] == 2100 and n_2100 is None: n_2100 = j

    # 2. Saldo (comes right after nominal or near it)
    # Search for saldo text after n_idx
    s_idx = None
    s_split = None
    s_txt = ""
    s_2206 = None
    s_2100 = None
    for j in range(n_idx + 1, min(len(doc.records), n_idx + 45)):
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            try:
                t = r['payload'].decode('utf-16le').rstrip('\x00')
                if any(c.isdigit() for c in t) and ('.' in t or ',' in t) and not t.startswith('+') and not t.startswith('-'):
                    s_idx = j
                    s_txt = t
                    # check next split
                    if j + 5 < len(doc.records) and doc.records[j+5]['tag'] in (2201, 2202):
                        t_split = doc.records[j+5]['payload'].decode('utf-16le').rstrip('\x00')
                        if t_split in ('00', ',00', '7,00', '04,00'):
                            s_split = j + 5
                            s_txt += t_split
                    break
            except:
                pass
    if s_idx:
        for j in range(s_idx - 15, s_idx):
            if doc.records[j]['tag'] == 2206: s_2206 = j
        for j in range(s_idx, s_idx + 15):
            if doc.records[j]['tag'] == 2100 and s_2100 is None: s_2100 = j

    # 3. Row number (comes before n_idx)
    no_idx = None
    no_split = None
    no_txt = ""
    for j in range(n_idx - 70, n_idx - 10):
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            try:
                t = r['payload'].decode('utf-16le').rstrip('\x00')
                if t.isdigit() and len(t) <= 2:
                    # check if next node is also digit
                    no_idx = j
                    no_txt = t
                    if j + 5 < len(doc.records) and doc.records[j+5]['tag'] in (2201, 2202):
                        t2 = doc.records[j+5]['payload'].decode('utf-16le').rstrip('\x00')
                        if t2.isdigit() and len(t2) <= 2:
                            no_split = j + 5
                            no_txt += t2
            except:
                pass

    # 4. Tanggal & Jam (search after row, or before next row)
    # Search for 'Nov 2025' or 'WIB'
    d_nodes = []
    t_nodes = []
    for j in range(n_idx, min(len(doc.records), n_idx + 120)):
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            try:
                t = r['payload'].decode('utf-16le').rstrip('\x00')
                if 'Nov' in t or '2025' in t or 'Des' in t:
                    d_nodes.append((j, t))
                elif 'WIB' in t or ':' in t and len(t) <= 15:
                    t_nodes.append((j, t))
            except:
                pass
        if len(d_nodes) >= 1 and len(t_nodes) >= 1:
            # check if we reached next row
            pass

    row_maps[row_num] = {
        'row_num': row_num,
        'no': {'idx': no_idx, 'split': no_split, 'txt': no_txt},
        'nom': {'idx': n_idx, 'split': n_split, 'txt': n_txt, '2206': n_2206, '2100': n_2100, '150': n_150},
        'sal': {'idx': s_idx, 'split': s_split, 'txt': s_txt, '2206': s_2206, '2100': s_2100},
        'tgl': d_nodes[:2],
        'jam': t_nodes[:2]
    }

print("=== ALL 22 ROWS MAPPED ===")
for r_num in sorted(row_maps.keys()):
    rm = row_maps[r_num]
    print(f"Row {r_num:2d}: No={rm['no']} | Nom={rm['nom']} | Sal={rm['sal']} | Tgl={rm['tgl']} | Jam={rm['jam']}")
