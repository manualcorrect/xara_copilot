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
    # Find preceding Tag 150
    for j in range(idx - 1, max(0, idx - 20), -1):
        if doc.records[j]['tag'] == 150:
            return j, doc.records[j]['payload'].hex()
    return None, None

def get_matrix(idx):
    # Find preceding Tag 2100
    for j in range(idx - 1, max(0, idx - 25), -1):
        if doc.records[j]['tag'] == 2100:
            p = doc.records[j]['payload']
            if len(p) >= 12:
                x, y, f = struct.unpack('<iii', p[:12])
                return j, x, y, f
    return None, None, None, None

def get_kern(idx):
    # Find preceding Tag 2206
    for j in range(idx - 1, max(0, idx - 10), -1):
        if doc.records[j]['tag'] == 2206:
            p = doc.records[j]['payload']
            if len(p) >= 12:
                w, h, dx = struct.unpack('<iii', p[:12])
                return j, w, h, dx
    return None, None, None, None

# Let's inspect headers:
headers_map = {
    "page1": {
        "cabang": 935,
        "periode_nodes": [961, 965, 973, 978], # '0', '1', 'Sep 2025 - 30 Sep 202', '5'
        "dicetak_nodes": [989, 993, 1001], # '0', '2', 'Nov 2025'
        "rekening": 1031, # '1630014643020 '
        "page_header": 1210, # '1 dari 10'
        "page_footer": 1079, # 'of 10'
        "customer_name": 3083, # 'YULIANA SANI PUTRI'
        "saldo_awal": [1101, 1106], # '654.', '955,00 '
        "dana_masuk": [1115, 1120, 1125], # '+ ', '16.872.668,', '00'
        "dana_keluar": [1137, 1142], # '- 17.502.', '777,00 '
        "saldo_akhir": [1154, 1159], # '24.846,', '00'
    },
    "page2": {
        "cabang": 3596,
        "periode_nodes": [3622, 3626, 3634, 3639],
        "dicetak_nodes": [3650, 3654, 3662],
        "page_header": 3728, # 'dari 10'
        "page_footer": 3695, # 'of 10'
        "customer_name": 5945, # 'YULIANA SANI PUTRI'
    },
    "page3": {
        "cabang": 6458,
        "periode_nodes": [6484, 6488, 6496, 6501],
        "dicetak_nodes": [6512, 6516, 6524],
        "page_header": 6590, # 'dari 10'
        "page_footer": 6557, # 'of 10'
        "customer_name": 8964, # 'YULIANA SANI PUTRI'
    }
}

print("=== VERIFYING HEADERS MAP ===")
for p, h in headers_map.items():
    print(f"\n--- {p} ---")
    for k, v in h.items():
        if isinstance(v, list):
            vals = [f"Rec {idx}: {repr(get_txt(idx))}" for idx in v]
            print(f"  {k}: {vals}")
        else:
            print(f"  {k}: Rec {v}: {repr(get_txt(v))}")
