import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Let's inspect the exact sequence for each of the 22 rows
# We will identify the nominal record, and from it find:
# - n_2100, n_150, n_2206, n_txt, n_split
# - s_2100, s_150, s_2206, s_txt, s_split
# - row_no_recs
# - jam_recs
# - tgl_recs

nom_recs = [1587, 1778, 1949, 2115, 2316, 2477, 2643, 2823, 3014, 3192,
            4215, 4401, 4587, 4753, 4929, 5114, 5300, 5471, 5632, 5808, 5994, 6160]

row_maps_verified = []

for idx, n_idx in enumerate(nom_recs, 1):
    # Nominal text
    n_rec = doc.records[n_idx]
    n_txt = n_rec['payload'].decode('utf-16le').rstrip('\x00')
    
    # n_2206
    n_2206 = n_idx - 1
    assert doc.records[n_2206]['tag'] == 2206, f"Row {idx}: n_2206 not tag 2206 at {n_2206}"
    
    # n_150
    n_150 = None
    for j in range(n_2206 - 15, n_2206):
        if doc.records[j]['tag'] == 150:
            n_150 = j
            break
            
    # n_2100
    n_2100 = None
    for j in range(n_150 - 15, n_150):
        if doc.records[j]['tag'] == 2100:
            n_2100 = j
            break
            
    # n_split
    n_split = None
    # Check if node right after n_idx is text and part of nominal
    if doc.records[n_idx + 5]['tag'] in (2201, 2202):
        t_cand = doc.records[n_idx + 5]['payload'].decode('utf-16le').rstrip('\x00')
        if t_cand in ('00,00', '00', ',00', '7,00'):
            n_split = n_idx + 5
            n_txt += t_cand
            
    # Saldo search after nominal
    # First find s_2100 after n_split or n_idx
    search_start = (n_split if n_split else n_idx) + 1
    s_2100 = None
    s_150 = None
    s_2206 = None
    s_txt_idx = None
    s_split = None
    s_txt = ""
    
    for j in range(search_start, search_start + 35):
        if doc.records[j]['tag'] == 2100 and s_2100 is None:
            s_2100 = j
        elif doc.records[j]['tag'] == 150 and s_150 is None:
            s_150 = j
        elif doc.records[j]['tag'] == 2206 and s_2206 is None:
            s_2206 = j
        elif doc.records[j]['tag'] in (2201, 2202) and s_txt_idx is None:
            try:
                t = doc.records[j]['payload'].decode('utf-16le').rstrip('\x00')
                if any(c.isdigit() for c in t) and ('.' in t or ',' in t) and not t.startswith('+') and not t.startswith('-'):
                    s_txt_idx = j
                    s_txt = t
                    if doc.records[j + 5]['tag'] in (2201, 2202):
                        t_sp = doc.records[j + 5]['payload'].decode('utf-16le').rstrip('\x00')
                        if t_sp in ('00', ',00', '7,00', '04,00'):
                            s_split = j + 5
                            s_txt += t_sp
                    break
            except:
                pass
            
    # Row Number: search backwards from n_2100
    no_nodes = []
    for j in range(n_2100 - 60, n_2100 - 5):
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            try:
                t = r['payload'].decode('utf-16le').rstrip('\x00')
                if t.isdigit() and len(t) <= 2:
                    no_nodes.append((j, t))
            except:
                pass
    # We want the last 1 or 2 digit nodes before n_2100
    # Usually the row number is right before the description
    
    # Jam: search after s_txt_idx
    search_jam = (s_split if s_split else s_txt_idx) + 1
    jam_nodes = []
    tgl_nodes = []
    for j in range(search_jam, search_jam + 60):
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            try:
                t = r['payload'].decode('utf-16le').rstrip('\x00')
                if 'WIB' in t or ':' in t and len(t) <= 15:
                    jam_nodes.append((j, t))
                elif 'Nov' in t or '2025' in t or 'Des' in t:
                    tgl_nodes.append((j, t))
            except:
                pass
                
    row_maps_verified.append({
        'row': idx,
        'nom': {'2100': n_2100, '150': n_150, '2206': n_2206, 'txt_idx': n_idx, 'split': n_split, 'txt': n_txt},
        'sal': {'2100': s_2100, '150': s_150, '2206': s_2206, 'txt_idx': s_txt_idx, 'split': s_split, 'txt': s_txt},
        'no_candidates': no_nodes[-2:] if len(no_nodes) >= 2 else no_nodes,
        'jam': jam_nodes,
        'tgl': tgl_nodes
    })

print("=== VERIFIED 22 ROW MAPPINGS ===")
for rm in row_maps_verified:
    print(f"Row {rm['row']:2d}:")
    print(f"  Nom: 2100={rm['nom']['2100']}, 150={rm['nom']['150']}, 2206={rm['nom']['2206']}, txt={rm['nom']['txt_idx']} ('{rm['nom']['txt']}'), split={rm['nom']['split']}")
    print(f"  Sal: 2100={rm['sal']['2100']}, 150={rm['sal']['150']}, 2206={rm['sal']['2206']}, txt={rm['sal']['txt_idx']} ('{rm['sal']['txt']}'), split={rm['sal']['split']}")
    print(f"  No : {rm['no_candidates']}")
    print(f"  Jam: {rm['jam']}")
    print(f"  Tgl: {rm['tgl']}")
