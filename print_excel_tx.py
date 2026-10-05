import json
import struct
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
excel_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\Template_Pekerjaan_Xara_Jul.xlsx"

doc = XarDocument(xar_path)
cfg = parse_xara_excel_template(excel_path)

def get_text(idx):
    if 0 <= idx < len(doc.records):
        r = doc.records[idx]
        if r['tag'] in (2201, 2202, 2203):
            return r['payload'].decode('utf-16le', errors='ignore')
    return ""

def get_color(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 150:
        return doc.records[idx]['payload'].hex()
    return None

def get_pos(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2100:
        coords = struct.unpack('<iii', doc.records[idx]['payload'][:12])
        return coords[0], coords[1]
    return None

def get_kern(idx):
    if 0 <= idx < len(doc.records) and doc.records[idx]['tag'] == 2206:
        m = struct.unpack('<iii', doc.records[idx]['payload'][:12])
        return m[0], m[1]
    return None

print("=== EXCEL TRANSACTIONS ===")
for i, tx in enumerate(cfg['transactions']):
    print(f"Row {i+1:2d}: Date={tx.get('tgl')} Time={tx.get('jam')} Keterangan={repr(tx.get('uraian'))} Nominal={tx.get('nominal')} ({tx.get('tipe')}) Saldo={tx.get('saldo')}")

