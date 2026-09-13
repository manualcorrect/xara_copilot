from xar_dom_engine import XarDocument

out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0_output.xar'
doc = XarDocument(out_path)

print("=== AUDIT DOM 0_OUTPUT.XAR (JUL 2026) ===")
print(f"Total records: {len(doc.records)}")

# 1. Header Nama
p1_nama = doc.records[937]['payload'].decode('utf-16le').rstrip('\x00')
p2_nama = doc.records[3755]['payload'].decode('utf-16le').rstrip('\x00')
print(f"[*] Nama Nasabah: P1='{p1_nama}' | P2='{p2_nama}'")

# 2. Header Periode
p1_per = doc.records[995]['payload'].decode('utf-16le') + doc.records[999]['payload'].decode('utf-16le') + doc.records[1007]['payload'].decode('utf-16le') + doc.records[1012]['payload'].decode('utf-16le')
print(f"[*] Periode P1  : '{p1_per}'")

# 3. Header Dicetak
p1_cetak = doc.records[1023]['payload'].decode('utf-16le') + doc.records[1027]['payload'].decode('utf-16le') + doc.records[1035]['payload'].decode('utf-16le')
p2_cetak = doc.records[3857]['payload'].decode('utf-16le') + doc.records[3861]['payload'].decode('utf-16le') + doc.records[3869]['payload'].decode('utf-16le')
print(f"[*] Tanggal Cetak: P1='{p1_cetak}' | P2='{p2_cetak}'")

# 4. Nomor Rekening
acc = doc.records[1065]['payload'].decode('utf-16le').rstrip('\x00')
print(f"[*] Rekening    : '{acc}'")

# 5. Nomor Halaman
h1_of = doc.records[1117]['payload'].decode('utf-16le') + doc.records[1122]['payload'].decode('utf-16le')
h1_dari = doc.records[1232]['payload'].decode('utf-16le')
h2_of = doc.records[3894]['payload'].decode('utf-16le') + " " + doc.records[3902]['payload'].decode('utf-16le')
h2_dari = doc.records[3927]['payload'].decode('utf-16le') + " " + doc.records[3935]['payload'].decode('utf-16le')
print(f"[*] Halaman P1  : '{h1_of}' | '{h1_dari}'")
print(f"[*] Halaman P2  : '{h2_of}' | '{h2_dari}'")

# 6. Summary
sawal = doc.records[1142]['payload'].decode('utf-16le')
dmasuk = doc.records[1468]['payload'].decode('utf-16le')
dkeluar = doc.records[1163]['payload'].decode('utf-16le')
sakhir = doc.records[1176]['payload'].decode('utf-16le')
print(f"[*] Ringkasan   : Awal='{sawal}' | Masuk='{dmasuk}' | Keluar='{dkeluar}' | Akhir='{sakhir}'")

# 7. Table Rows
print("\n[*] Tabel Mutasi 22 Baris Transaksi:")
from test_jul_profile import row_table_7395
for idx in range(1, 23):
    m = row_table_7395[idx]
    no_str = "".join([doc.records[r]['payload'].decode('utf-16le').rstrip('\x00') for r, _ in m['no_nodes']])
    d_str = doc.records[m['d_rec']]['payload'].decode('utf-16le').rstrip('\x00')
    nom_str = doc.records[m['nom']['txt']]['payload'].decode('utf-16le').rstrip('\x00')
    sal_str = doc.records[m['sal']['txt']]['payload'].decode('utf-16le').rstrip('\x00')
    col_nom = doc.records[m['nom']['150']]['payload'].hex()
    col_sal = doc.records[m['sal']['150']]['payload'].hex()
    print(f"  Baris {idx:2d}: No={no_str:2s} | Tgl={d_str} | Nom={nom_str:>14s} (col={col_nom}) | Saldo={sal_str:>14s} (col={col_sal})")
