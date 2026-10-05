import os
import json
import struct
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
excel_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\Template_Pekerjaan_Xara_Jul.xlsx"

doc = XarDocument(xar_path)
cfg = parse_xara_excel_template(excel_path)

with open("candidate_tx_nodes.json", "r", encoding="utf-8") as f:
    nodes = json.load(f)

# Helper functions
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

# Let's inspect every row in 0.xar.
# In 0.xar, the 34 original nominal values are:
# Row 1: -500.000,00
# Row 2: -14.000,00
# Row 3: +510.000,00
# ...
# Let's find each row by searching for the amount pattern and date/time pattern!

# Let's write a script that identifies the exact 34 rows and prints their mapped structure
rows_map = []

# Let's trace through all nodes and extract:
# (row_no, date_nodes, time_nodes, nominal_nodes, saldo_nodes)
# Notice in each row:
# Date is like: '01 Sep 20' (Tag 2201) + '25' (Tag 2201/2202)
# Time is like: '4:12:29 WIB' (Tag 2201) or '02:40:58' + 'WIB'
# Nominal is like: '-500.000,00' or '+519.000,' + '00'
# Saldo is like: '154.9' + '55,00' or '120.955' + ',00'

# Let's find all nominal nodes first
nominal_candidates = []
for i, n in enumerate(nodes):
    txt = n['text']
    if any(c in txt for c in ['+', '-']) and any(c in txt for c in [',', '.']) and ('WIB' not in txt) and ('Sep' not in txt) and ('Jul' not in txt):
        nominal_candidates.append(i)

print(f"Found {len(nominal_candidates)} nominal candidate nodes.")
for c in nominal_candidates:
    print(f"Node {c}: Rec {nodes[c]['idx']} -> {repr(nodes[c]['text'])}")
