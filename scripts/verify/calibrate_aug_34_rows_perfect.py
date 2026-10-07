import os
import json
import struct
from xar_dom_engine import XarDocument

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar"
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

# Definitive 34 Rows Mapping for 10,429-record 0.xar in Aug
# Let's inspect all 34 rows:
# Page 1: Rows 1..10
# Page 2: Rows 11..22
# Page 3: Rows 23..34

aug_rows = [
    # Page 1 (Rows 1..10)
    {"row_no": 1, "nom": [1529], "saldo": [1549, 1554], "time": [1574], "date": [1594, 1599]},
    {"row_no": 2, "nom": [1686], "saldo": [1706, 1711], "time": [1731], "date": [1751, 1756]},
    {"row_no": 3, "nom": [1844], "saldo": [1864, 1869], "time": [1889], "date": [1909, 1914]},
    {"row_no": 4, "nom": [2021], "saldo": [2041, 2046], "time": [2066], "date": [2086, 2091]},
    {"row_no": 5, "nom": [2198], "saldo": [2218, 2223], "time": [2243], "date": [2263, 2268]},
    {"row_no": 6, "nom": [2387, 2392], "saldo": [2412, 2417], "time": [2432], "date": [2452]},
    {"row_no": 7, "nom": [2544, 2549], "saldo": [2574], "time": [2594], "date": [2614]},
    {"row_no": 8, "nom": [2731], "saldo": [2751, 2756], "time": [2776], "date": [2796]},
    {"row_no": 9, "nom": [2888], "saldo": [2908, 2913], "time": [2933], "date": [2953]},
    {"row_no": 10, "nom": [3078, 3083], "saldo": [3103], "time": [3123], "date": [3143]},

    # Page 2 (Rows 11..22)
    {"row_no": 11, "nom": [4045, 4050], "saldo": [4070], "time": [4090], "date": [4110]},
    {"row_no": 12, "nom": [4190], "saldo": [4210, 4215], "time": [4235], "date": [4255]},
    {"row_no": 13, "nom": [4362, 4367], "saldo": [4392, 4397], "time": [4417], "date": [4437]},
    {"row_no": 14, "nom": [4529], "saldo": [4549, 4554], "time": [4579], "date": [4599]},
    {"row_no": 15, "nom": [4687], "saldo": [4707, 4712], "time": [4732], "date": [4752]},
    {"row_no": 16, "nom": [4844], "saldo": [4864, 4869], "time": [4889], "date": [4909]},
    {"row_no": 17, "nom": [5012], "saldo": [5032, 5037], "time": [5062], "date": [5082]},
    {"row_no": 18, "nom": [5185], "saldo": [5205, 5210], "time": [5230], "date": [5250]},
    {"row_no": 19, "nom": [5357], "saldo": [5377, 5382], "time": [5407], "date": [5427]},
    {"row_no": 20, "nom": [5534, 5539], "saldo": [5559, 5564], "time": [5589], "date": [5609, 5614]},
    {"row_no": 21, "nom": [5732], "saldo": [5752, 5757], "time": [5777], "date": [5797, 5802]},
    {"row_no": 22, "nom": [5890], "saldo": [5910, 5915], "time": [5935], "date": [5955, 5960]},

    # Page 3 (Rows 23..34)
    {"row_no": 23, "nom": [6942], "saldo": [6962, 6967], "time": [6987], "date": [7007]},
    {"row_no": 24, "nom": [7095, 7100], "saldo": [7120], "time": [7140], "date": [7160]},
    {"row_no": 25, "nom": [7248], "saldo": [7268, 7273], "time": [7298], "date": [7318]},
    {"row_no": 26, "nom": [7446, 7451], "saldo": [7471, 7476], "time": [7496], "date": [7516, 7521]},
    {"row_no": 27, "nom": [7604, 7609], "saldo": [7629, 7634], "time": [7654], "date": [7674]},
    {"row_no": 28, "nom": [7757], "saldo": [7777, 7782], "time": [7802], "date": [7822]},
    {"row_no": 29, "nom": [7920], "saldo": [7940, 7945], "time": [7965], "date": [7985]},
    {"row_no": 30, "nom": [8073, 8078], "saldo": [8098, 8103], "time": [8123], "date": [8143]},
    {"row_no": 31, "nom": [8241], "saldo": [8261, 8266], "time": [8286], "date": [8306]},
    {"row_no": 32, "nom": [8398], "saldo": [8418, 8423], "time": [8443], "date": [8463]},
    {"row_no": 33, "nom": [8556], "saldo": [8576, 8581], "time": [8601], "date": [8621]},
    {"row_no": 34, "nom": [8718], "saldo": [8738, 8743], "time": [8763], "date": [8783, 8788]},
]

verified_aug_map = []
print("=== VERIFYING AUG 34 ROWS ===")
for r in aug_rows:
    nom_txt = "".join(get_txt(i) for i in r['nom'])
    saldo_txt = "".join(get_txt(i) for i in r['saldo'])
    time_txt = "".join(get_txt(i) for i in r['time'])
    date_txt = "".join(get_txt(i) for i in r['date'])

    nom_p = r['nom'][0]
    saldo_p = r['saldo'][0]

    # Ensure nom_p and saldo_p are Tag 2201 (TAG_TEXT_STRING)
    assert doc.records[nom_p]['tag'] == 2201, f"Row {r['row_no']} nom_p {nom_p} is not Tag 2201! (Got Tag {doc.records[nom_p]['tag']})"
    assert doc.records[saldo_p]['tag'] == 2201, f"Row {r['row_no']} saldo_p {saldo_p} is not Tag 2201! (Got Tag {doc.records[saldo_p]['tag']})"

    verified_aug_map.append({
        "row_no": r['row_no'],
        "nom_primary": nom_p,
        "nom_splits": r['nom'][1:],
        "nom_tag150": get_tag150(nom_p),
        "nom_tag2100": get_tag2100(nom_p),
        "nom_tag2206": get_tag2206(nom_p),
        "saldo_primary": saldo_p,
        "saldo_splits": r['saldo'][1:],
        "saldo_tag150": get_tag150(saldo_p),
        "saldo_tag2100": get_tag2100(saldo_p),
        "saldo_tag2206": get_tag2206(saldo_p),
        "time_primary": r['time'][0],
        "time_splits": r['time'][1:],
        "date_primary": r['date'][0],
        "date_splits": r['date'][1:],
        "orig_nom": nom_txt,
        "orig_saldo": saldo_txt,
        "orig_time": time_txt,
        "orig_date": date_txt
    })
    print(f"Row {r['row_no']:02d}: Nom={repr(nom_txt):15s} | Saldo={repr(saldo_txt):15s} | Time={repr(time_txt):15s} | Date={repr(date_txt)}")

with open("perfect_aug_34_rows_map.json", "w", encoding="utf-8") as f:
    json.dump(verified_aug_map, f, indent=2)

print("\nSaved perfect_aug_34_rows_map.json successfully!")
