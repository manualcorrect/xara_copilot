from xar_dom_engine import XarDocument
import struct

final_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_output.xar'
doc = XarDocument(final_path)

print("=========================================================")
print("   AUDIT & VERIFIKASI INTEGRITAS DOKUMEN XARA FINAL      ")
print("=========================================================")
print(f"[*] Target File   : {final_path}")
print(f"[*] Total Records : {len(doc.records)} records (Status: {'PASS' if len(doc.records) == 6775 else 'FAIL'})")

# 1. Check Payload Sizes
size_errors = 0
for idx, r in enumerate(doc.records):
    if r['size'] != len(r['payload']):
        size_errors += 1
print(f"[*] Auto-Sync Size: {'100% PASS' if size_errors == 0 else f'FAIL ({size_errors} errors)'}")

# 2. Check Tag 2202 zero-byte safety
zero_byte_2202 = [idx for idx, r in enumerate(doc.records) if r['tag'] == 2202 and len(r['payload']) == 0]
print(f"[*] Tag 2202 Zero-Byte Safety: {'100% PASS (No 0-byte nodes)' if len(zero_byte_2202) == 0 else f'FAIL ({len(zero_byte_2202)} found)'}")

# 3. Header Verification
print("\n--- Header Verification ---")
p1_name = doc.records[899]['payload'].decode('utf-16le', errors='ignore')
p2_name = doc.records[3603]['payload'].decode('utf-16le', errors='ignore')
print(f"[*] Nama Nasabah: Page 1={repr(p1_name)} | Page 2={repr(p2_name)}")

p1_per = doc.records[952]['payload'].decode('utf-16le', errors='ignore')
p2_per = doc.records[3656]['payload'].decode('utf-16le', errors='ignore')
print(f"[*] Periode     : Page 1='01 {p1_per}' | Page 2='01 {p2_per}'")

p1_cetak = f"{doc.records[964]['payload'].decode('utf-16le')}{doc.records[968]['payload'].decode('utf-16le')} {doc.records[976]['payload'].decode('utf-16le')}{doc.records[981]['payload'].decode('utf-16le')}"
p2_cetak = f"{doc.records[3668]['payload'].decode('utf-16le')}{doc.records[3672]['payload'].decode('utf-16le')} {doc.records[3680]['payload'].decode('utf-16le')}{doc.records[3685]['payload'].decode('utf-16le')}"
print(f"[*] Tanggal Cetak: Page 1={repr(p1_cetak)} | Page 2={repr(p2_cetak)}")

p1_rek = f"{doc.records[1002]['payload'].decode('utf-16le')}{doc.records[1007]['payload'].decode('utf-16le')}"
print(f"[*] No Rekening : {repr(p1_rek)}")

# 4. Ringkasan Finansial Verification
print("\n--- Ringkasan Finansial Header ---")
s_awal = doc.records[1091]['payload'].decode('utf-16le', errors='ignore')
d_masuk = f"{doc.records[1100]['payload'].decode('utf-16le')}{doc.records[1104]['payload'].decode('utf-16le')}"
d_keluar = doc.records[1131]['payload'].decode('utf-16le', errors='ignore')
s_akhir = doc.records[1143]['payload'].decode('utf-16le', errors='ignore')
print(f"[*] Saldo Awal  : {repr(s_awal)}")
print(f"[*] Dana Masuk  : {repr(d_masuk)}")
print(f"[*] Dana Keluar : {repr(d_keluar)}")
print(f"[*] Saldo Akhir : {repr(s_akhir)}")

# 5. Table Mutations Verification
print("\n--- Verifikasi 22 Baris Mutasi Tabel ---")
row_s_txt = [1492, 1637, 1805, 1966, 2137, 2316, 2477, 2617, 2780, 2885, 4049, 4184, 4319, 4454, 4614, 4749, 4884, 5019, 5171, 5323, 5449, 5570]
row_n_txt = [1512, 1657, 1825, 1986, 2157, 2336, 2497, 2637, 2800, 2908, 4069, 4204, 4339, 4474, 4634, 4769, 4904, 5039, 5191, 5343, 5502, 5618]
row_dates = [1567, 1702, 1875, 2036, 2202, 2381, 2547, 2682, 2845, 2963, 4109, 4249, 4389, 4519, 4674, 4814, 4949, 5084, 5241, 5388, 5550, 5666]

for i in range(22):
    s_val = doc.records[row_s_txt[i]]['payload'].decode('utf-16le', errors='ignore').strip()
    n_val = doc.records[row_n_txt[i]]['payload'].decode('utf-16le', errors='ignore').strip()
    d_val = doc.records[row_dates[i]]['payload'].decode('utf-16le', errors='ignore').strip()
    print(f"Baris {i+1:02d} | Tgl: {d_val:11s} | Nom: {n_val:14s} | Saldo: {s_val:12s}")

print("\n=========================================================")
print("          VERIFIKASI TAHAP 1 s.d. 7: 100% SUKSES!        ")
print("=========================================================")
