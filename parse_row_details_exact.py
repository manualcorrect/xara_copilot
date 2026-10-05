import json
import struct
from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

def get_txt(idx):
    if 0 <= idx < len(doc.records):
        r = doc.records[idx]
        if r['tag'] in (2201, 2202, 2203):
            return r['payload'].decode('utf-16le', errors='ignore')
    return ""

def get_pos(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2100:
        return struct.unpack('<iii', doc.records[idx]['payload'][:12])
    return None

def get_kern(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2206:
        return struct.unpack('<iii', doc.records[idx]['payload'][:12])
    return None

def get_color(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 150:
        return doc.records[idx]['payload'].hex()
    return None

# Let's inspect Row 1:
# Row 1 text nodes:
# No: Rec 1521 '1'
# Ket: Rec 1541 'Penarikan tun', Rec 1546 'ai', Rec 1551 ' di ATM', Rec 1557 'BANK MAND', Rec 1562 'I', Rec 1567 'RI SRG AM BHAYANGKARA'
# Saldo: Rec 1588 '54.048,00'
# Nominal: Rec 1609 '-700.0', Rec 1614 '00,00'
# Time: Rec 1634 '07:09:03 WIB'
# Date: Rec 1654 '01 Nov 2025'

# Let's write an automated exact analyzer for all 19 rows
# Let's find for each row:
# - Saldo text rec, kern rec, pos rec, color rec
# - Nominal text rec, split rec, kern rec, pos rec, color rec
# - Time text rec(s)
# - Date text rec(s)

row_info = []

# List of all row start numbers
row_nums = [
    (1, 1521), (2, 1694), (3, 1856), (4, 2028), (5, 2205),
    (6, 2382), (7, 2509), (8, 2676), (9, 2892), (10, 3029),
    (11, 4138), (12, 4282), (13, 4424), (14, 4566), (15, 4713),
    (16, 4885), (17, 5007), (18, 5200), (19, 5312)
]

for idx in range(len(row_nums)):
    r_num, start_rec = row_nums[idx]
    end_rec = row_nums[idx+1][1] if idx+1 < len(row_nums) else 5430
    
    # Within start_rec..end_rec find elements:
    s_txt = None
    s_kern = None
    s_pos = None
    s_col = None
    
    n_txt = None
    n_split = None
    n_kern = None
    n_pos = None
    n_col = None
    
    d_recs = []
    t_recs = []
    
    for r in range(start_rec, end_rec):
        txt = get_txt(r)
        
        # Check if Date
        if 'Nov 2025' in txt or 'Nov 202' in txt or (len(txt) == 1 and txt in '0123456789' and any('Nov' in get_txt(r+offset) for offset in range(-5, 6))):
            d_recs.append((r, txt))
        # Check if Time
        elif 'WIB' in txt or 'WI' in txt or (':' in txt and any('WIB' in get_txt(r+offset) for offset in range(1, 4))):
            t_recs.append((r, txt))
        # Check if Saldo / Nominal
        elif ',00' in txt or ',0' in txt or (txt.startswith('-') or txt.startswith('+')):
            # Determine whether Saldo or Nominal based on position or appearance
            # Saldo always appears before Nominal in the DOM structure for these rows
            if s_txt is None:
                s_txt = r
                # Find kern and pos before s_txt
                for k in range(r-1, max(start_rec, r-15), -1):
                    if doc.records[k]['tag'] == 2206 and s_kern is None:
                        s_kern = k
                    if doc.records[k]['tag'] == 2100 and s_pos is None:
                        s_pos = k
                    if doc.records[k]['tag'] == 150 and s_col is None:
                        s_col = k
            else:
                if n_txt is None:
                    n_txt = r
                    for k in range(r-1, s_txt, -1):
                        if doc.records[k]['tag'] == 2206 and n_kern is None:
                            n_kern = k
                        if doc.records[k]['tag'] == 2100 and n_pos is None:
                            n_pos = k
                        if doc.records[k]['tag'] == 150 and n_col is None:
                            n_col = k
                elif n_split is None:
                    n_split = r

    row_info.append({
        'row': r_num,
        's_txt': s_txt,
        's_txt_val': get_txt(s_txt),
        's_kern': s_kern,
        's_pos': s_pos,
        's_col': s_col,
        'n_txt': n_txt,
        'n_txt_val': get_txt(n_txt),
        'n_split': n_split,
        'n_split_val': get_txt(n_split) if n_split else None,
        'n_kern': n_kern,
        'n_pos': n_pos,
        'n_col': n_col,
        'd_recs': d_recs,
        't_recs': t_recs
    })

print(json.dumps(row_info, indent=2))
with open('row_info_6707.json', 'w', encoding='utf-8') as f:
    json.dump(row_info, f, indent=2)

