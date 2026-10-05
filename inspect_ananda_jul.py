import json
from xar_dom_engine import XarDocument
from parse_excel_template import parse_xara_excel_template

xar_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
excel_path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\Template_Pekerjaan_Xara_Jul.xlsx"

doc = XarDocument(xar_path)
cfg = parse_xara_excel_template(excel_path)

print(f"Total records: {len(doc.records)}")
print("Excel Header:", cfg['header'])
print("Excel Summary:", cfg['summary'])
print("Excel Tx Count:", len(cfg['transactions']))

text_nodes = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202, 2203):
        try:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if txt.strip():
                text_nodes.append((i, r['tag'], txt))
        except:
            pass

print(f"Total text nodes: {len(text_nodes)}")
with open("ananda_jul_texts.json", "w", encoding="utf-8") as f:
    json.dump([{"idx": idx, "tag": tag, "text": txt} for idx, tag, txt in text_nodes], f, indent=2, ensure_ascii=False)

for item in text_nodes:
    idx, tag, txt = item
    if any(k in txt for k in ['ANANDA', 'PT', '16400', 'Jul', '2026', 'IDR', 'Saldo', 'CABANG', 'Cabang', '1 of', 'dari', 'Page', 'Lembar', 'Halaman', '01 ', '31 ', '54-']):
        print(f"Rec {idx:4d} (Tag {tag:4d}): {repr(txt)}")
