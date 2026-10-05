import os
import json
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
doc = XarDocument(xar_path)

def get_txt(idx):
    try:
        return doc.records[idx]['payload'].decode('utf-16le')
    except:
        return ""

def get_color(idx):
    for j in range(idx - 1, max(0, idx - 25), -1):
        if doc.records[j]['tag'] == 150:
            return j, doc.records[j]['payload'].hex()
    return None, None

def get_matrix(idx):
    for j in range(idx - 1, max(0, idx - 25), -1):
        if doc.records[j]['tag'] == 2100:
            p = doc.records[j]['payload']
            if len(p) >= 12:
                x, y, f = struct.unpack('<iii', p[:12])
                return j, x, y, f
    return None, None, None, None

def get_kern(idx):
    for j in range(idx - 1, max(0, idx - 10), -1):
        if doc.records[j]['tag'] == 2206:
            p = doc.records[j]['payload']
            if len(p) >= 12:
                w, h, dx = struct.unpack('<iii', p[:12])
                return j, w, h, dx
    return None, None, None, None

# Find all 34 rows
# Let's inspect the page blocks:
# Page 1: Rows 1..10
# Page 2: Rows 11..22
# Page 3: Rows 23..34

print("=== SCANNING ALL 34 ROWS ===")
# We know the nominal records from our earlier scan
# Let's locate each row's components:
# row_no, nominal_nodes, saldo_nodes, time_nodes, date_nodes

# Let's build a scanner that groups each row
# Let's search for row number nodes
row_targets = []
# Row 1 to 34
for i in range(1, 35):
    str_num = str(i)
    # find where this number appears in Tag 2201 or 2202 in row order
    # Let's search texts
    pass

# Let's dump all text records by page with their indices
all_tx_nodes = []
for i in range(1200, 8950):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        txt = get_txt(i)
        all_tx_nodes.append((i, r['tag'], txt))

print(f"Total candidate text nodes: {len(all_tx_nodes)}")
# Save all candidate text nodes to a json for precise mapping
with open("candidate_tx_nodes.json", "w", encoding="utf-8") as f:
    json.dump([{"idx": t[0], "tag": t[1], "text": t[2]} for t in all_tx_nodes], f, indent=2)

print("Saved candidate_tx_nodes.json.")
