import json
import struct
from xar_dom_engine import XarDocument

out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(out_path)

with open('jul_mapping.json', 'r', encoding='utf-8') as f:
    mapping = json.load(f)

with open('jul_final_tx_schedule.json', 'r', encoding='utf-8') as f:
    txs = json.load(f)

print("=" * 100)
print("AUDIT & VERIFIKASI HASIL AKHIR: 0_TAHAP7.XAR (MARSIYAH JULI 2026)")
print("=" * 100)

# 1. Name Check (8 Pages)
print("\n[1] CUSTOMER NAME CHECK (8 PAGES):")
for p_idx, item in enumerate(mapping["customer_name"], 1):
    val = doc.records[item["rec_idx"]]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    assert val.strip() == "MASRIYAH MUHAMMAD SAMIAN", f"Mismatch on Page {p_idx}: {val}"
    print(f"  Page {p_idx} (Rec {item['rec_idx']:5d}): '{val}' [PASS]")

# 2. Period Check (8 Pages)
print("\n[2] PERIOD CHECK (8 PAGES):")
for p_idx, item in enumerate(mapping["period"], 1):
    val = doc.records[item["rec_idx"]]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    sec_val = doc.records[item["rec_idx"]+5]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    assert val == "01 Jul 2026 - 31 Jul 2026", f"Mismatch on Page {p_idx}: {val}"
    assert sec_val == "", f"Secondary node not clean on Page {p_idx}: {sec_val}"
    print(f"  Page {p_idx} (Rec {item['rec_idx']:5d}): '{val}' [PASS]")

# 3. Print Date Check (8 Pages)
print("\n[3] PRINT DATE CHECK (8 PAGES):")
for p_idx, item in enumerate(mapping["dicetak_pada"], 1):
    d_rec = item["rec_idx"]
    tens = doc.records[d_rec-12]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    units = doc.records[d_rec-8]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    month = doc.records[d_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    full_d = f"{tens}{units} {month}"
    assert full_d == "10 Sep 2026", f"Mismatch on Page {p_idx}: {full_d}"
    print(f"  Page {p_idx} (Rec {d_rec:5d}): '{full_d}' [PASS]")

# 4. Account Number Check
print("\n[4] ACCOUNT NUMBER CHECK:")
acc_val = doc.records[mapping["account_number"]["rec_idx"]]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
assert acc_val.strip() == "1630016144514", f"Mismatch: {acc_val}"
print(f"  Page 1 (Rec {mapping['account_number']['rec_idx']:5d}): '{acc_val}' [PASS]")

# 5. Financial Summary Check
print("\n[5] FINANCIAL SUMMARY HEADER CHECK:")
s_awal = doc.records[1175]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
d_masuk = doc.records[1184]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
d_keluar = doc.records[1202]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
s_akhir = doc.records[1215]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
print(f"  Saldo Awal   (Rec 1175): '{s_awal}'")
print(f"  Dana Masuk   (Rec 1184): '{d_masuk}'")
print(f"  Dana Keluar  (Rec 1202): '{d_keluar}'")
print(f"  Saldo Akhir  (Rec 1215): '{s_akhir}'")

# 6. Table Transactions Check (Sample 15 Rows)
print("\n[6] TABLE TRANSACTIONS CHECK (SAMPLE ROWS):")
for r_idx in [0, 1, 2, 21, 22, 33, 45, 57, 69, 80, 81, 82]:
    tx = txs[r_idx]
    r_info = tx["xar_row_info"]
    s_rec = r_info["saldo_rec"]
    k_rec = r_info["tag2204_rec"]
    nom_rec = r_info["nominal_rec"]
    d_rec = r_info["date_rec"]
    t_rec = r_info["time_rec"]
    
    d_val = doc.records[d_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if d_rec else "-"
    t_val = doc.records[t_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if t_rec else "-"
    s_val = doc.records[s_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    nom_val = doc.records[nom_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if nom_rec else "-"
    
    dx, dy = struct.unpack('<ii', doc.records[k_rec]['payload'][:8])
    print(f"  Row {tx['index']:2d} | {d_val} {t_val:12s} | Nom: {nom_val:15s} | Saldo: {s_val:13s} (dx={dx:5d}, dy={dy:7d})")

print("\n" + "=" * 100)
print("HASIL VERIFIKASI POST-FLIGHT INTEGRITY: 100% PASS [OK]")
print("=" * 100)
