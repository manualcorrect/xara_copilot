# 📜 MASTER PROSEDUR STANDAR TAHAP 7: PERUBAHAN RINGKASAN & TABEL TRANSAKSI UTAMA

Document Version: 2.0 (Project V2 Official Permanent Standard)  
Status: **PERMANENT MASTER STANDARD**  
Environment: Xara Designer Pro+ Binary Format (`.xar`)  
Target Output: `test_v2.1_tahap7.xar` (dari input `test_v2.1_tahap6.xar`)

---

## 📌 1. DEFINISI & TUJUAN TAHAP 7
**Tahap 7** adalah tahap pengubahan seluruh angka keuangan utama dokumen rekening koran (*e-Statement*), meliputi:
1. **Ringkasan Header**:
   - Saldo Awal (`Rec 1148`)
   - Dana Masuk (`Rec 1158`)
   - Dana Keluar (`Rec 1176`)
   - Saldo Akhir (`Rec 1195`)
2. **Tabel Transaksi Utama (17 Baris)**:
   - Nominal Transaksi (Kredit `+` / Debit `-`)
   - Saldo Akhir Berjalan (*Running Balance*)

---

## 🎨 2. STANDAR PEWARNAAN AKURAT (`TAG 150`)

Setiap angka memiliki atribut warna `Tag 150` yang **wajib mengunci** palet resmi dokumen:

| Objek | Nilai Warna Biner (`Tag 150`) | Kode Hex | Tampilan Visual |
| :--- | :---: | :---: | :---: |
| **Nominal Kredit (`+`)** | `b'\xcf\x03\x00\x00'` | `#00A651` | **Hijau** |
| **Nominal Debit (`-`)** | `b'\x1e\x02\x00\x00'` | `#000000` | **Hitam** |
| **Saldo Berjalan (*Running Balance*)** | `b'\x1a\x05\x00\x00'` | `#005B9C` | **Biru** |
| **Header Saldo Awal** | `b'\x57\x03\x00\x00'` | `#333333` | **Abu Gelap / Hitam** |
| **Header Dana Masuk** | `b'\xcf\x03\x00\x00'` | `#00A651` | **Hijau** |
| **Header Dana Keluar** | `b'\x1e\x02\x00\x00'` | `#000000` | **Hitam** |
| **Header Saldo Akhir** | `b'\x1a\x05\x00\x00'` | `#005B9C` | **Biru** |

---

## 🛡️ 3. PRESERVASI TYPOGRAPHY & FONT NATIVE TAHAP 6

* **Proteksi Mutlak Font Definition**: Blok record biner definisi font dokumen (Record 0 s.d. 1100, termasuk `Tag 2000`, `Tag 4350`, `Tag 4351`, `Tag 4352`) **DILARANG DISISIPI MAUPUN DIUBAH**.
* **Keutuhan Huruf a-z**: Seluruh huruf a-z, uraian transaksi, teks disclaimer, header tabel, dan metadata dipertahankan 100% dari basis dokumen `test_v2.1_tahap6.xar` yang murni. Hal ini mencegah Xara memicu reset font fallback (`PDF-PDF-PDF-PDF-PD`).
* **Kerapian Ukuran Record**: Setiap record teks yang diubah wajib selalu disinkronkan `rec["size"] = len(rec["payload"])` guna mencegah *streaming read error*.

---

## 🧹 4. PEMBERSIHAN PECAHAN SEKUNDER (*SPLIT RECORD CLEANUP*)

Untuk mencegah angka sisa bertumpuk (*ghost digits*):

1. **Pembersihan Ringkasan Header**:
   - Secondary Dana Masuk (`Rec 1163`): Wajib di-set ke `b'\x00\x00'` (mencegah munculnya `.000`).
   - Secondary Dana Keluar (`Rec 1177` & `Rec 1182`): Wajib di-set ke `b'\x00\x00'` (mencegah munculnya `.0000`).
   - Saldo Awal: String `"654.955,00 "` dikunci bersih tanpa karakter `-` atau `+`.

2. **Pembersihan Tabel Transaksi (17 Baris)**:
   - Seluruh record sekunder pada kolom Nominal dan Saldo (misalnya `Rec 1715`, `Rec 1720`, `Rec 1729`, `Rec 4385`, `Rec 4389`, `Rec 4398`, dll.) wajib di-set ke `b'\x00\x00'` (`size = 2`).

---

## ⚙️ 5. ARSITEKTUR SCRIPT RESMI

Eksekusi permanen Tahap 7 diotomatisasi melalui skrip resmi:
* **Script Eksekusi**: `apply_tahap_7_tabel_ringkasan.py`
* **Log Verifikasi**: `training_history.json`
* **File Output Master**: `C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar` (Total record persis 6908 records).
