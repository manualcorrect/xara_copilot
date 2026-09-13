from xar_dom_engine import XarDocument
import struct

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# Let's inspect Header Dana Masuk (1275) & Dana Keluar (1292)
for rec_idx in [1275, 1292]:
    # Look backwards for Tag 2100 and Tag 2206
    t2100 = None
    t2206 = None
    for j in range(rec_idx-15, rec_idx):
        if doc.records[j]['tag'] == 2100:
            t2100 = (j, struct.unpack('<iii', doc.records[j]['payload']))
        if doc.records[j]['tag'] == 2206:
            t2206 = (j, struct.unpack('<iii', doc.records[j]['payload']))
    txt = doc.records[rec_idx]['payload'].decode('utf-16le', errors='replace')
    print(f"Header Rec {rec_idx} ({repr(txt)}):")
    print(f"  Tag 2100: {t2100}")
    print(f"  Tag 2206: {t2206}")

# Let's inspect Rows 29 to 36
rows_to_check = [
    ("Row 29 Saldo", 8336),
    ("Row 29 Nominal", 8357),
    ("Row 30 Saldo", 8490),
    ("Row 31 Saldo", 8663),
    ("Row 32 Saldo", 8800),
    ("Row 32 Nominal", 8821),
    ("Row 33 Saldo", 8907),
    ("Row 33 Nominal", 8928),
    ("Row 34 Saldo", 9044),
    ("Row 34 Nominal", 9065),
    ("Row 35 Saldo", 10189),
    ("Row 35 Nominal", 10210),
    ("Row 36 Nominal", 10367),
]

print("\n--- TABLE ROWS COORDINATES ---")
for label, rec_idx in rows_to_check:
    t2100 = None
    t2206 = None
    for j in range(rec_idx-15, rec_idx):
        if doc.records[j]['tag'] == 2100:
            t2100 = (j, struct.unpack('<iii', doc.records[j]['payload']))
        if doc.records[j]['tag'] == 2206:
            t2206 = (j, struct.unpack('<iii', doc.records[j]['payload']))
    txt = doc.records[rec_idx]['payload'].decode('utf-16le', errors='replace')
    print(f"{label:15s} Rec {rec_idx} ({repr(txt):16s}):")
    print(f"  Tag 2100: {t2100}")
    print(f"  Tag 2206: {t2206}")
