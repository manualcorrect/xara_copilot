import json
import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar")

def get_txt(idx):
    try:
        return doc.records[idx]['payload'].decode('utf-16le')
    except:
        return ""

def get_tag150(idx):
    for j in range(idx - 1, max(0, idx - 25), -1):
        if doc.records[j]['tag'] == 150:
            return j
    return None

def get_tag2100(idx):
    for j in range(idx - 1, max(0, idx - 25), -1):
        if doc.records[j]['tag'] == 2100:
            return j
    return None

def get_tag2206(idx):
    for j in range(idx - 1, max(0, idx - 10), -1):
        if doc.records[j]['tag'] == 2206:
            return j
    return None

# Let's find all nominals and saldos across the entire 0.xar
# In Aug 0.xar, each transaction row has:
# [Row No] -> [Keterangan] -> [Nominal] -> [Saldo] -> [Time] -> [Date]

# Let's collect all text stories between 1450 and 8800
stories = []
for i in range(1450, 8800):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        txt = get_txt(i)
        stories.append({'idx': i, 'tag': r['tag'], 'text': txt})

# Let's identify the 34 rows
# We know the nominal values in original 0.xar:
# Row 1: -20.000,00
# Row 2: -49.700,00
# Row 3: +400.000,00
# Row 4: -50.000,00
# Row 5: -350.000,00
# Row 6: +64.400,00 (or +64.400, + 00)
# Row 7: -64.500,00 (or -64.500, + 00)
# Row 8: +80.000,00
# Row 9: -80.003,00
# Row 10: +60.139,00
# ...
# Let's trace through stories and extract each row cleanly

# Let's locate the 34 Nominal nodes:
nom_nodes_found = []
for s in stories:
    txt = s['text'].strip()
    idx = s['idx']
    if (txt.startswith('+') or txt.startswith('-')) and any(c.isdigit() for c in txt) and ('WIB' not in txt) and ('Sep' not in txt):
        nom_nodes_found.append((idx, txt, s['tag']))

print(f"Found {len(nom_nodes_found)} nominal nodes:")
for n in nom_nodes_found:
    print(f"  Rec {n[0]:5d} (Tag {n[2]}): {n[1]}")
