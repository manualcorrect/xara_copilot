import json
import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar")

# Let's inspect colors
# Saldo Awal color: around Rec 1100
# Dana Masuk color: around Rec 1115
# Dana Keluar color: around Rec 1135
# Saldo Akhir color: around Rec 1155

print("=== SUMMARY HEADER NODES (Rec 1090 - 1165) ===")
for i in range(1090, 1165):
    r = doc.records[i]
    tag = r['tag']
    p = r['payload']
    if tag == 150:
        print(f"Rec {i:05d} (Tag 150): {p.hex()}")
    elif tag in (2201, 2202):
        print(f"Rec {i:05d} (Tag {tag}): {repr(p.decode('utf-16le'))}")

# Check table nominal and saldo colors
print("\n=== TRANSACTION ROW COLORS ===")
# CR color
cr_c = doc.records[1833]['payload'].hex() # Row 3 (+400.000,00)
db_c = doc.records[1518]['payload'].hex() # Row 1 (-20.000,00)
saldo_c = doc.records[1543]['payload'].hex() # Row 1 Saldo
print(f"Kredit (+) Color    : {cr_c}")
print(f"Debit (-) Color     : {db_c}")
print(f"Saldo Berjalan Color: {saldo_c}")
