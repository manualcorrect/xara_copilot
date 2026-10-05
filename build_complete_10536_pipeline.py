import os
import json
import struct
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\0.xar"
excel_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Jul\Template_Pekerjaan_Xara_Jul.xlsx"

doc = XarDocument(xar_path)
cfg = parse_xara_excel_template(excel_path)

print(f"Loaded XAR with {len(doc.records)} records.")
print(f"Parsed Excel with {len(cfg['transactions'])} transactions.")

# Let's find all rows: Row numbers 1 to 34
row_records = {}

# In Mandiri statements, each row has:
# - No (1..34)
# - Date (e.g. 01 Sep 2025)
# - Time (e.g. 08:30:00 WIB)
# - Keterangan
# - Nominal (e.g. +500.000,00 or -14.000,00)
# - Saldo (e.g. 154.955,00)

def decode_text(p):
    try:
        return p.decode('utf-16le').strip()
    except:
        return ""

# Let's inspect all records that contain row numbers or amounts
texts = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202, 2208, 2209):
        txt = decode_text(r['payload'])
        if txt:
            texts.append((i, r['tag'], txt))

print(f"Total non-empty text records: {len(texts)}")

# Print transactions structure
tx_list = []
# Let's trace transactions by looking for nominal patterns (+..., -...) and saldos
for idx, (rec_idx, tag, txt) in enumerate(texts):
    if (txt.startswith("+") or txt.startswith("-")) and ("," in txt or "." in txt):
        print(f"Found Nominal at Rec {rec_idx:05d}: {txt}")
        # Look around for row context
        context = texts[max(0, idx-5):min(len(texts), idx+6)]
        print("   Context:", " | ".join([f"[{t[0]}:{t[2]}]" for t in context]))
