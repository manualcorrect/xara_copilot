# MASTER SOP PROJECT V2: AI Agent Asisten Pengeditan Dokumen Xara (.xar)

Document Version: 1.0 (Project V2 Official Standard)  
Status: Permanent Master Standard Operating Procedure  
Environment: Xara Designer Pro+ Binary Format (`.xar`)  

---

## I. VISI UTAMA & PRINSIP DASAR KINERJA AGENT

1. **Tujuan Utama**: Membangun Asisten AI Agent untuk meningkatkan produktivitas pengolahan dokumen e-Statement/PDF secara presisi dan konsisten.
2. **Kelebihan Format Xara (`.xar`)**: Pengeditan dilakukan melalui file biner `.xar` karena Xara mampu **menyunting teks menggunakan font yang bahkan TIDAK TERINSTALL di Windows**, dengan tetap menghasilkan bentuk font, style, warna, dan ukuran yang 100% konsisten visualnya.
3. **PRINSIP WAJIB EKSEKUSI**: **Perubahan WAJIB dilakukan SATU-PER-SATU secara berurutan per-tahap** demi mencegah error dan menjamin stabilitas biner dokumen.

---

## II. ALUR PROSEDUR PENGEDITAN 7 TAHAP

```mermaid
flowchart TD
    A[File Input .xar Masuk] --> T1[Tahap 1: Perubahan Nama]
    T1 --> T2[Tahap 2: Perubahan Periode]
    T2 --> T3[Tahap 3: Perubahan Dicetak Pada]
    T3 --> T4[Tahap 4: Perubahan Nomor Rekening]
    T4 --> T5[Tahap 5: Perubahan Nomor Halaman]
    T5 --> T6[Tahap 6: Perubahan Tanggal Sesuai Periode & Jam]
    T6 --> T7[Tahap 7: Perubahan Saldo Awal, Dana Masuk, Dana Keluar, Saldo Akhir, Nominal, & Saldo]
    T7 --> B[Hasil Output .xar Sempurna & Terverifikasi]
```

### **TAHAP 1: Perubahan Nama**
* **Target**: Mengubah nama nasabah/pemilik rekening (`Nama/Name`) pada seluruh halaman.
* **Standar Layout & Format**:
  - String Nama **WAJIB** diakhiri dengan spasi dan newline `\r\n` (contoh: `f"{NAMA_BARU} \r\n"`).
  - Mekanisme ini mengaktifkan line-break internal pada text story container Xara, memindahkan **Nama ke Baris 1 (Atas)** dan **Cabang ke Baris 2 (Bawah)**.
  - Tag Kerning 2206 setelah record Nama di-set `Kern X = 0` agar alignment Cabang di baris 2 pas dan konsisten.
* **Aturan**: Eksekusi khusus nama saja, tanpa menyentuh field lain.

### **TAHAP 2: Perubahan Periode**
* **Target**: Mengubah rentang tanggal laporan (`Periode/Period`) pada seluruh halaman header (contoh: `01 Dec 2026 - 31 Dec 2026`).
* **Standar Layout & Node Structure**:
  - String periode header terpisah menjadi 4 record node biner per halaman:
    1. **Bulan/Tahun Awal + Separator**: `"[MMM YYYY] - "` (Halaman 1: Rec 01022, Halaman 2: Rec 03988)
    2. **Digit Puluhan Tanggal Akhir**: `"[D]"` (Halaman 1: Rec 01023, Halaman 2: Rec 03989)
    3. **Digit Satuan Tanggal Akhir + Spasi**: `"[D] "` (Halaman 1: Rec 01028, Halaman 2: Rec 03994)
    4. **Bulan/Tahun Akhir**: `"[MMM YYYY]"` (Halaman 1: Rec 01033, Halaman 2: Rec 03999)
  - **Sinkronisasi Otomatis**: Pengubahan bulan wajib menghitung otomatis jumlah hari dalam bulan tersebut (contoh: Dec = 31 hari) dan memperbarui ke-8 record node tersebut secara bersamaan.
* **Aturan**: Eksekusi khusus periode header saja, tanggal transaksi tabel dikerjakan di Tahap 6.

### **TAHAP 3: Perubahan Dicetak Pada**
* **Target**: Mengubah tanggal penerbitan dokumen (`Dicetak pada/Issued on`) pada seluruh halaman.
* **Standar Layout & Node Structure**:
  - String tanggal cetak terpisah menjadi 2 record node biner per halaman:
    1. **Tanggal & Bulan + Trailing Space**: `"[DD MMM ]"` (Halaman 1: Rec 03222, Halaman 2: Rec 06281)
    2. **Tahun 4 Digit**: `"[YYYY]"` (Halaman 1: Rec 03227, Halaman 2: Rec 06286)
  - **Sinkronisasi**: Pengubahan tanggal cetak wajib meng-update ke-4 node tersebut secara bersamaan pada seluruh halaman.

### **TAHAP 4: Perubahan Nomor Rekening**
* **Target**: Mengubah nomor rekening nasabah (`Nomor Rekening/Account Number`) pada header dokumen.
* **Standar Layout & Node Structure**:
  - Nomor Rekening berada secara eksklusif pada Header Halaman 1 (`Rec 01054`).
  - **Trailing Space Mandatory**: String nomor rekening **WAJIB** mempertahankan spasi penutup `f"{NOMOR_REKENING} "` agar kerning dan spacing header tetap presisi.
* **Aturan**: Eksekusi khusus nomor rekening saja.

### **TAHAP 5: Perubahan Nomor Halaman**
* **Target**: Mengubah penomoran halaman dinamis (`Page X of Y` / `X dari Y`) pada Header dan Footer seluruh halaman.
* **Standar Layout & Node Structure (Sinkronisasi 4 Node Wajib)**:
  1. **Page 1 Header**: `Rec 01278` -> `f"ari {TOTAL_PAGES}"` (membentuk `1 dari Y`)
  2. **Page 1 Footer**: `Rec 01125` -> `f"1 of {TOTAL_PAGES}"` (membentuk `1 of Y`)
  3. **Page 2 Header**: `Rec 04080` -> `f"ari {TOTAL_PAGES}"` (membentuk `2 dari Y`)
  4. **Page 2 Footer**: `Rec 04033` -> `f"of {TOTAL_PAGES}"` (membentuk `2 of Y` dipasangkan dengan `Rec 04025`)
* **Rule Mandatory**: Perubahan total halaman **WAJIB** meng-update ke-4 node tersebut sekaligus agar Header (`X dari Y`) dan Footer (`X of Y`) 100% sinkron secara visual.

### **TAHAP 6: Perubahan Tanggal Sesuai Periode & Jam**
* **Target**: Mengubah tanggal transaksi (disesuaikan dengan periode header) dan timestamp jam (`HH:MM:SS WIB`) pada setiap baris transaksi tabel.
* **Standar Layout & Format**:
  - **Period Matching Mandatory**: Seluruh tanggal baris transaksi **WAJIB** berada dalam rentang bulan & tahun periode yang dikunci di Tahap 2 (contoh: `Dec 2026`).
  - **24-Hour Time Format & Kerning Protection**: Format timestamp jam **WAJIB** menggunakan sistem 24 jam (`HH:MM:SS WIB`). Untuk string bawaan biner yang memiliki kerning X terkunci untuk 1-digit jam (seperti `1:20:13 WIB` pada Baris 5 atau `3:59:00 WIB` pada Baris 17), panjang string asli **WAJIB dipertahankan** (`1:20:13 WI` / `3:59:00 WIB`) agar penambahan digit tidak menggeser bounding box ke kiri dan tidak terjadi overlap secara visual.
  - **Pengujian Baris Spesifik**: Pengubahan baris tertentu (contoh: Baris 10 `25 Dec 2026 04:00:00`) dilakukan langsung pada record date & time pasangan baris tersebut tanpa merusak kerning baris lain.

### **TAHAP 7: Perubahan Ringkasan & Tabel Transaksi Utama (FINAL)**
* **Target**: Mengubah data angka ringkasan header dan tabel transaksi secara utuh berdasarkan data input tabel user:
  1. **Saldo Awal / Initial Balance** (Rec 01148)
  2. **Dana Masuk / Incoming Transactions** (Rec 01158)
  3. **Dana Keluar / Outgoing Transactions** (Rec 01176)
  4. **Saldo Akhir / Closing Balance** (Rec 01195)
  5. **Nominal Kredit (`+`) / Debit (`-`) tiap baris**
  6. **Saldo Akhir Berjalan (*Running Balance*) tiap baris**
* **Standar Pewarnaan Jenis Transaksi & Saldo (Color Rule)**:
  - **Kredit (`+` / Dana Masuk)**: Nominal diawali tanda `+` dan `Tag 150` di-set ke **HIJAU** (`b'\xcf\x03\x00\x00'`, #00A651).
  - **Debit (`-` / Dana Keluar)**: Nominal diawali tanda `-` dan `Tag 150` di-set ke **HITAM** (`b'\x1e\x02\x00\x00'`, #000000).
  - **Saldo Berjalan (*Running Balance*)**: `Tag 150` wajib mempertahankan warna **BIRU** (`b'\x1a\x05\x00\x00'`, #005B9C).
  - **Ringkasan Header**: Saldo Awal (Dark Gray `b'\x57\x03\x00\x00'`), Dana Masuk (Hijau `b'\xcf\x03\x00\x00'`), Dana Keluar (Hitam `b'\x1e\x02\x00\x00'`), Saldo Akhir (Biru `b'\x1a\x05\x00\x00'`).
* **Split Record Cleanup Rule (Pembersihan Overlap & Ghost Digits)**:
  - Pada dokumen biner Xara, string nominal, saldo berjalan, serta ringkasan dana masuk/keluar terpecah menjadi *primary record* dan *secondary split records*.
  - **Rule Mandatory**: Nilai string baru dimasukkan ke *primary record*, dan seluruh *secondary split records* **WAJIB dibersihkan ke string kosong `""` (`b'\x00\x00'`)**:
    - **Tabel Transaksi**: `Rec 1720`, `Rec 1729`, `Rec 4385`, `Rec 4389`, `Rec 4398`, dll.
    - **Ringkasan Header**: Secondary Dana Masuk (`Rec 1163`) dan Secondary Dana Keluar (`Rec 1177`, `Rec 1182`) wajib di-clear agar tidak muncul digit '0' berlebih (seperti `6.360.206,000` atau `-4.072.500,0000`).
* **Standar Rata Kanan Kolom (Right-Alignment Rule on Ruler & Grid)**:
  - **Koordinat Acuan Sisi Kanan Resmi**:
    - **Kolom Nominal ($X_{\text{right}}$)**: **`15.214 cm`** (`431.267 millipoints`).
    - **Kolom Saldo ($X_{\text{right}}$)**: **`20.049 cm`** (`568.306 millipoints`).
  - **Mekanisme Perhitungan Dinamis Sumbu X Xara**:
    Sistem teks Xara memposisikan teks dari sisi kiri ($X_{\text{left}}$ / `Tag 2100 Matrix X`), sedangkan kolom tabel akuntansi menganut rata kanan ($X_{\text{right}}$). Agar sisi kanan seluruh baris transaksi sejajar tegak lurus sempurna, nilai $X_{\text{left}}$ wajib dihitung mundur:
    $$X_{\text{left}} = X_{\text{target\_right}} - W(\text{teks})$$
    $$\text{Line Advance Width (Tag 2206)} = W(\text{teks})$$
  - **Tabel Metrik Lebar Font Biner Resmi (*Glyph Advance Widths*)**:
    - Digit: `'0'`: 5438 mp, `'1'`: 3160 mp, `'2'`: 4762 mp, `'3'`: 4840 mp, `'4'`: 5039 mp, `'5'`: 4840 mp, `'6'`: 4878 mp, `'7'`: 4402 mp, `'8'`: 4962 mp, `'9'`: 4878 mp.
    - Simbol & Tanda Baca: `'.'`: 1840 mp, `','`: 1243 mp, `'-'`: 3198 mp, `'+'`: 4399 mp, `' '`: 2200 mp.
  - Setiap perubahan nominal dan saldo wajib meng-update pasangan `Tag 2100` ($X_{\text{left}}$) dan `Tag 2206` ($W$) secara serempak.
* **Standar Bentuk Font Angka 0-9 & Zero-Shift Glyph Replacement**:
  - **Font Utama Angka**: Seluruh angka Nominal, Saldo, dan Ringkasan menggunakan **`TTInterphases-Bold`** (Font ID 13, `Tag 2907 = 444`).
  - **Bentuk Angka 0 s.d. 8**: Menggunakan kurva vektor tebal bawaan murni dari Font ID 13.
  - **Bentuk Angka 9 Bold Sempurna**: Disesuaikan persis mengikuti kurva vektor tebal pada `test_3.1.xar` (826 bytes).
  - **Zero-Shift In-Place Replacement Rule (Aturan Mutlak Tanpa Injeksi Record)**:
    - Format biner Xara menggunakan sistem pointer indeks record absolut untuk memanggil atribut warna (`Tag 150`) dan font (`Tag 2907`).
    - **Dilarang keras menyisipkan (*insert*) record baru** ke dalam stream karena akan menggeser ribuan record setelahnya dan merusak seluruh pointer warna menjadi hitam serta mereset font dokumen.
    - Penyesuaian angka 9 dilakukan dengan menimpa (*in-place replace*) Record 343 (`Tag 4350`, glyph `'A'` yang tidak digunakan pada font bold) dengan payload kurva angka 9 bold (826 bytes).
    - Dengan metode ini, total record dokumen **terkunci stabil persis 6.908 record**, seluruh angka 0–9 berbobot tebal sempurna, dan pointer warna/font tidak bergeser satu angka pun.
* **Preservasi Tipografi Teks Non-Angka**:
  - Tipe font teks (huruf a-z, uraian transaksi, nama nasabah, judul dokumen, dan metadata) **WAJIB 100% mempertahankan font bawaan murni dari Tahap 6**.
  - Nilai `Tag 2907` pada cerita teks deskripsi dilarang disentuh agar tidak memicu dialog reset fallback (`PDF-PDF-PDF...`).

---

## III. ATURAN PENERAPAN BINER & UKURAN PAYLOAD

Saat melakukan pengubahan teks pada setiap tahap di atas:
* **Auto-Size Sync**: Nilai header record biner `rec["size"]` **WAJIB selalu disinkronkan** dengan `len(rec["payload"])` agar tidak memicu `A read error occurred (streaming error)` di Xara.
* **Tag 2202 Atomic Character Node Rule (Pembersihan Split Record)**: Tag 2202 (`TAG_TEXT_CHAR` / `TAG_TEXT_EOL`) dan Tag 2201 **DILARANG bernilai 0 byte (`b''`)**. Pembersihan node split sekunder **WAJIB menggunakan payload 2-byte null character `b'\x00\x00'`** (`rec["size"] = 2`). Payload 0 byte akan menyebabkan Xara crash dengan pesan `Failed to handle record [rec] 2202 (This file is corrupted and unreadable)`.
* **Font Definition Lock**: `Tag 2907` pada node definisi font dilarang diubah agar embedded font bawaan dokumen tidak ter-reset.
* **Zero-Shift Pointer Mandate**: Dilarang menambah atau menghapus record. Total record dokumen wajib terkunci konstan (6.908 pada test 2 halaman, 14.392 pada test 5 halaman).

