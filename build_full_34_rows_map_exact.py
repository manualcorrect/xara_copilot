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

def get_tag2204(idx):
    for j in range(idx - 1, max(0, idx - 10), -1):
        if doc.records[j]['tag'] == 2204:
            return j
    return None

# Let's map each of the 34 rows by inspecting the sequence:
# Each row contains:
# [Row No] -> [Keterangan description lines] -> [Nominal primary node (+ split node)] -> [Saldo primary node (+ split node)] -> [Time primary node (+ split node)] -> [Date primary node (+ split node)]

# Let's write an intelligent row extractor that finds each row by its sequential row number
rows_map = []

# Row boundaries:
# We know:
# Row 1: No at 1433, Nom at [1453], Saldo at [1473, 1478], Time at [1498], Date at [1518, 1523]
# Row 2: No at 1563, Nom at [1609, 1614], Saldo at [1634], Time at [1654, 1659], Date at [1679, 1684]
# Row 3: No at 1761, Nom at [1781, 1786], Saldo at [1806, 1811], Time at [1831], Date at [1851, 1856]
# Row 4: No at 1901, Nom at [1952], Saldo at [1972, 1977], Time at [1997], Date at [2017, 2022]

# Let's find all row number nodes (1 to 34):
# On Page 1 (1..10):
# On Page 2 (11..22):
# On Page 3 (23..34):

# Let's scan all rows systematically
current_row = 1
# Let's search all records between 1300 and 8950
for r_no in range(1, 35):
    # Find row number
    pass

print("=== BUILDING PRECISE 34 ROW MAPPINGS ===")
# Let's collect all text stories between 1300 and 8920
stories = []
current_story = []
for i in range(1300, 8920):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2208, 2209):
        txt = get_txt(i)
        stories.append({
            'idx': i,
            'tag': r['tag'],
            'text': txt,
            'tag150': get_tag150(i),
            'tag2100': get_tag2100(i),
            'tag2206': get_tag2206(i),
            'tag2204': get_tag2204(i)
        })

print(f"Total text nodes in transactions area: {len(stories)}")
with open("extracted_all_stories.json", "w", encoding="utf-8") as f:
    json.dump(stories, f, indent=2)

print("Saved extracted_all_stories.json.")
