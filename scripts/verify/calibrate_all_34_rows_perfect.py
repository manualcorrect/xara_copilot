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

# Definitive 34 Rows Mapping for 10,536-record 0.xar
rows_exact = [
    # Row 1
    {"row_no": 1, "nom": [1453], "saldo": [1473, 1478], "time": [1498], "date": [1518, 1523]},
    # Row 2
    {"row_no": 2, "nom": [1609, 1614], "saldo": [1634], "time": [1654, 1659], "date": [1679, 1684]},
    # Row 3
    {"row_no": 3, "nom": [1781, 1786], "saldo": [1806, 1811], "time": [1831], "date": [1851, 1856]},
    # Row 4
    {"row_no": 4, "nom": [1952], "saldo": [1972, 1977], "time": [1997], "date": [2017, 2022]},
    # Row 5
    {"row_no": 5, "nom": [2108], "saldo": [2128, 2133], "time": [2153], "date": [2173, 2178]},
    # Row 6
    {"row_no": 6, "nom": [2274], "saldo": [2294, 2299], "time": [2319], "date": [2339, 2344]},
    # Row 7
    {"row_no": 7, "nom": [2432], "saldo": [2452, 2457], "time": [2477], "date": [2497, 2502]},
    # Row 8
    {"row_no": 8, "nom": [2593], "saldo": [2613, 2618], "time": [2638], "date": [2658, 2663]},
    # Row 9
    {"row_no": 9, "nom": [2760], "saldo": [2780, 2785], "time": [2805], "date": [2825, 2830]},
    # Row 10
    {"row_no": 10, "nom": [2942], "saldo": [2962, 2967], "time": [2987], "date": [3007, 3012]},
    
    # Page 2: Rows 11 to 22
    # Row 11
    {"row_no": 11, "nom": [3971], "saldo": [3991, 3996], "time": [4016], "date": [4036, 4041]},
    # Row 12
    {"row_no": 12, "nom": [4124, 4129], "saldo": [4149, 4154], "time": [4174], "date": [4194, 4199]},
    # Row 13
    {"row_no": 13, "nom": [4287, 4292], "saldo": [4312, 4317], "time": [4337], "date": [4357, 4362]},
    # Row 14
    {"row_no": 14, "nom": [4454], "saldo": [4474, 4479], "time": [4499], "date": [4519, 4524]},
    # Row 15
    {"row_no": 15, "nom": [4612], "saldo": [4632, 4637], "time": [4657, 4662], "date": [4682, 4687]},
    # Row 16
    {"row_no": 16, "nom": [4799], "saldo": [4819], "time": [4839, 4844], "date": [4864, 4869]},
    # Row 17
    {"row_no": 17, "nom": [4952], "saldo": [4972, 4977], "time": [4997], "date": [5017, 5022]},
    # Row 18
    {"row_no": 18, "nom": [5110, 5115], "saldo": [5135, 5140], "time": [5160], "date": [5180, 5185]},
    # Row 19
    {"row_no": 19, "nom": [5277], "saldo": [5297, 5302], "time": [5322, 5327], "date": [5347, 5352]},
    # Row 20
    {"row_no": 20, "nom": [5455], "saldo": [5475, 5480], "time": [5500, 5505], "date": [5525, 5530]},
    # Row 21
    {"row_no": 21, "nom": [5637], "saldo": [5657, 5662], "time": [5682], "date": [5702, 5707]},
    # Row 22
    {"row_no": 22, "nom": [5805], "saldo": [5825, 5830], "time": [5850], "date": [5870, 5875]},

    # Page 3: Rows 23 to 34
    # Row 23
    {"row_no": 23, "nom": [6856], "saldo": [6876, 6881], "time": [6901], "date": [6921, 6926]},
    # Row 24
    {"row_no": 24, "nom": [7034, 7039], "saldo": [7059, 7064], "time": [7084], "date": [7104, 7109]},
    # Row 25
    {"row_no": 25, "nom": [7216, 7221], "saldo": [7241, 7246, 7251], "time": [7271, 7276], "date": [7296, 7301]},
    # Row 26
    {"row_no": 26, "nom": [7438, 7443], "saldo": [7463], "time": [7483], "date": [7503, 7508]},
    # Row 27
    {"row_no": 27, "nom": [7591], "saldo": [7611], "time": [7631], "date": [7651, 7656]},
    # Row 28
    {"row_no": 28, "nom": [7772], "saldo": [7792, 7797], "time": [7817], "date": [7837, 7842]},
    # Row 29
    {"row_no": 29, "nom": [7949], "saldo": [7969, 7974], "time": [7994], "date": [8014, 8019]},
    # Row 30
    {"row_no": 30, "nom": [8126], "saldo": [8146, 8151], "time": [8171], "date": [8191, 8196]},
    # Row 31
    {"row_no": 31, "nom": [8317], "saldo": [8337, 8342], "time": [8362], "date": [8382, 8387]},
    # Row 32
    {"row_no": 32, "nom": [8494], "saldo": [8514, 8519], "time": [8539], "date": [8559, 8564]},
    # Row 33
    {"row_no": 33, "nom": [8671], "saldo": [8691], "time": [8711], "date": [8731, 8736]},
    # Row 34
    {"row_no": 34, "nom": [8824], "saldo": [8844, 8849], "time": [8869], "date": [8889, 8894]},
]

print("=== VERIFYING EVERY SINGLE ROW ===")
verified_map = []
for r in rows_exact:
    nom_txt = "".join(get_txt(i) for i in r['nom'])
    saldo_txt = "".join(get_txt(i) for i in r['saldo'])
    time_txt = "".join(get_txt(i) for i in r['time'])
    date_txt = "".join(get_txt(i) for i in r['date'])
    
    nom_p = r['nom'][0]
    saldo_p = r['saldo'][0]
    
    verified_map.append({
        "row_no": r['row_no'],
        "nom_primary": nom_p,
        "nom_splits": r['nom'][1:],
        "nom_tag150": get_tag150(nom_p),
        "nom_tag2100": get_tag2100(nom_p),
        "nom_tag2206": get_tag2206(nom_p),
        "nom_tag2204": get_tag2204(nom_p),
        "saldo_primary": saldo_p,
        "saldo_splits": r['saldo'][1:],
        "saldo_tag150": get_tag150(saldo_p),
        "saldo_tag2100": get_tag2100(saldo_p),
        "saldo_tag2206": get_tag2206(saldo_p),
        "saldo_tag2204": get_tag2204(saldo_p),
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

with open("perfect_34_rows_map.json", "w", encoding="utf-8") as f:
    json.dump(verified_map, f, indent=2)

print("\nSaved perfect_34_rows_map.json successfully!")
