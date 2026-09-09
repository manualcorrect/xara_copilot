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

## 📐 5. STANDAR RATA KANAN TABEL (*RIGHT-ALIGNMENT STANDARD*)

Kolom **Nominal** dan **Saldo** wajib mengunci koordinat sisi kanan (*right-aligned*) berdasarkan grid dan ruler resmi:

### **A. Nilai Koordinat Acuan Sisi Kanan**
* **Kolom Nominal ($X_{\text{right}}$)**: **`15.214 cm`** (`431.267 millipoints`)
* **Kolom Saldo ($X_{\text{right}}$)**: **`20.049 cm`** (`568.306 millipoints`)

### **B. Formula Perhitungan Sumbu X Kiri ($X_{\text{left}}$)**
Karena sistem koordinat biner Xara (`Tag 2100 Matrix X`) memposisikan objek dari kiri:
$$X_{\text{left}} = X_{\text{target\_right}} - W(\text{teks})$$
$$\text{Line Advance Width (Tag 2206)} = W(\text{teks})$$

### **C. Tabel Metrik Advance Width Karakter Resmi (H = 6559 mp)**
| Karakter | Advance Width (mp) | Lebar dalam cm |
| :---: | :---: | :---: |
| `'0'` | `5438` | $0.192\text{ cm}$ |
| `'1'` | `3160` | $0.111\text{ cm}$ |
| `'2'` | `4762` | $0.168\text{ cm}$ |
| `'3'` | `4840` | $0.171\text{ cm}$ |
| `'4'` | `5039` | $0.173\text{ cm}$ |
| `'5'` | `4840` | $0.171\text{ cm}$ |
| `'6'` | `4878` | $0.172\text{ cm}$ |
| `'7'` | `4402` | $0.155\text{ cm}$ |
| `'8'` | `4962` | $0.175\text{ cm}$ |
| `'9'` | `4878` | $0.172\text{ cm}$ |
| `'.'` | `1840` | $0.065\text{ cm}$ |
| `','` | `1243` | $0.044\text{ cm}$ |
| `'-'` | `3198` | $0.113\text{ cm}$ |
| `'+'` | `4399` | $0.155\text{ cm}$ |
| `' '` | `2200` | $0.078\text{ cm}$ |

Setiap penyuntingan angka tabel wajib menyinkronkan `Tag 2100` ($X_{\text{left}}$) dan `Tag 2206` ($W$) menggunakan metrik di atas sehingga seluruh baris memiliki garis vertikal kanan yang persis 100% rata.

---

## 🔤 6. STANDAR BENTUK FONT ANGKA 0-9 & ZERO-SHIFT REPLACEMENT

* **Font Standar**: Seluruh angka tabel dan ringkasan wajib berbobot tebal (**`TTInterphases-Bold`**, Font ID 13, `Tag 2907 = 444`).
* **Angka 0 s.d. 8**: Menggunakan kurva vektor tebal bawaan murni dari Font ID 13.
* **Angka 9 Bold Sempurna**: Menggunakan definisi kurva vektor 826 bytes yang diekstrak dari acuan `test_3.1.xar`.
* **Aturan Mutlak Zero-Shift (*In-Place Replacement*)**:
  - Dilarang keras menyisipkan (*insert*) record baru karena format biner Xara menggunakan nomor urutan indeks absolut untuk pointer warna (`Tag 150`) dan font (`Tag 2907`). Injeksi record akan menggeser ribuan record setelahnya dan membuat semua warna menjadi hitam serta mereset font.
  - Penyesuaian angka 9 dilakukan secara *in-place replace* pada **Record 343** (menimpa glyph `'A'` yang tidak terpakai pada font bold).
  - Dengan metode ini, total record dokumen **terkunci stabil persis 6.908 record**, seluruh angka 0–9 tebal sempurna, dan pointer warna tetap utuh 100%.

---

## 🎨 7. STANDAR WARNA TRANSAKSI (TAG 150 COLOR RULES)

| Kategori Transaksi | Atribut Tag 150 | Nilai Biner Record | Record Target di Dokumen | Warna Tampilan |
| :--- | :---: | :---: | :---: | :---: |
| **Kredit (`+` / Masuk)** | `Tag 150` | `b'\xcf\x03\x00\x00'` | `Record 975` | **Hijau (`#00A651`)** |
| **Debit (`-` / Keluar)** | `Tag 150` | `b'\x1e\x02\x00\x00'` | `Record 542` | **Hitam (`#000000`)** |
| **Saldo Berjalan** | `Tag 150` | `b'\x1a\x05\x00\x00'` | `Record 1306` | **Biru (`#005B9C`)** |
| **Saldo Awal** | `Tag 150` | `b'\x57\x03\x00\x00'` | `Record 855` | **Dark Gray (`#333333`)** |

---

## ⚙️ 8. ARSITEKTUR SCRIPT RESMI

Eksekusi permanen Tahap 7 diotomatisasi melalui skrip resmi:
* **Script Eksekusi**: `apply_tahap_7_tabel_ringkasan.py`
* **Log Verifikasi**: `training_history.json`
* **File Output Master**: `C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar` (Total record persis 6.908 records, terkunci aman).
