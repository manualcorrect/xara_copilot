# MASTER KNOWLEDGE BASE: Prosedur Lengkap, Histori Error & Solusi, serta Hasil Training Manipulasi Dokumen Biner Xara (.xar)

Document Version: 2.0  
Status: Master Reference & Standard Operating Procedure (SOP)  
Target Environment: Xara Designer Pro+ Binary Format (`.xar`)  

---

## I. IKHTISAR SISTEM & STRUKTUR BINER XARA (`.xar`)

### 1. Anatomi Record Tag Utama

| Tag ID | Nama Tag | Deskripsi & Peran Kunci | Formula / Format Offset |
| :--- | :--- | :--- | :--- |
| **`2100`** | `TAG_MATRIX` | Record matriks transformasi (memuat koordinat $X$ dan $Y$ dalam *millipoints*). Dibaca langsung oleh **Toolbar Atas Xara GUI (`X: ... cm`)**. | Offset 0-3 / 40-47: Double $X$ & $Y$ dalam millipoints. |
| **`2206`** | `TAG_TEXT_KERN_X_Y` | Record kerning offset teks untuk render visual di viewport. | Offset 0-3: Int32 $X_{kern}$ ($1\text{ cm} = 28.346,457\text{ mp}$). |
| **`2207` / `2208` / `2209`** | `TAG_TEXT_STRING` | Record payload string teks (Latin1 atau UTF-16LE). | String buffer terminated by null byte. |
| **`150`** | `TAG_WEBCOLOR` | Record warna isian teks (*fill color*). | `f0030000` (Hijau `#00A651`), `61020000` (Hitam `#333333`), `4a040000` (Biru `#005B9C`). |
| **`2907`** | `TAG_FONT_REF` | Record referensi indeks font pada palet dokumen (`b7010000`). | **Dilarang diubah** pada node definisi font agar font tidak reset ke `PDF-PDF-PDF-PDF-PD`. |

---

### 2. Metrik Font & Formula Rata Kanan (*Right Alignment*)

* **Font Standard**: `TTInterphases-Bold.ttf` (8pt) & `TTInterphases-Regular.ttf` (8pt).
* **Konversi Skala**: $1\text{ cm} = 28.346,457\text{ millipoints}$.
* **Lebar Karakter Presisi**: $5.025\text{ millipoints} \approx 0,177\text{ cm}$ per karakter.
* **Formula Jangkar Kiri Dinamis ($X_{left\_new}$)**:
  $$X_{left\_new} = X_{right\_target} - (\text{Jumlah Karakter Baru} \times 5.025\text{ millipoints})$$
* **Koordinat Referensi Awal (*Ground-Truth Baseline*)**:
  * **Nominal Right Edge ($X_{right\_nominal}$)**: **$15,08\text{ cm}$** ($427.390\text{ millipoints}$) / **$15,18\text{ cm}$** ($430.300\text{ millipoints}$)
  * **Saldo Right Edge ($X_{right\_saldo}$)**: **$19,47\text{ cm}$** ($551.837\text{ millipoints}$)

---

## II. MATRIKS HISTORI ERROR, AKIBAT & SOLUSI TERUJI

| No | Gejala / Error | Penyebab Utama (*Root Cause*) | Solusi Teruji & Prosedur |
| :--- | :--- | :--- | :--- |
| **1** | **Teks Angka Menjadi Rata Kiri / Ujung Kanan Tidak Sejajar** | Mengubah teks tanpa menyesuaikan koordinat jangkar $X_{left}$ secara dinamis berdasarkan panjang string baru. | Terapkan **Tahap 8**: Hitung $X_{left\_new} = X_{right\_target} - (\text{Len} \times 0.177\text{ cm})$ lalu update `Tag 2100` dan `Tag 2206`. |
| **2** | **Nilai `X: ... cm` di Toolbar Atas Xara GUI Tidak Berubah / Berbeda dengan Render Visual** | Hanya meng-update `Tag 2206` (kerning) tanpa memperbarui `Tag 2100` (`TAG_MATRIX`). | Update berpasangan (*Dual-Tag Synchronization*): **`Tag 2100`** dan **`Tag 2206`** wajib di-update bersamaan. |
| **3** | **Font Ter-reset Menjadi `PDF-PDF-PDF-PDF-PD` / Warning Dialog Saat File Dibuka** | Mengubah record `Tag 2907` (`b7010000`) pada node definisi font dokumen. | Dilarang menyentuh `Tag 2907` pada node definisi font. Cukup ganti string `Tag 2207/2208/2209` dan warna `Tag 150`. |
| **4** | **Pergeseran Masal Kolom Saldo / Nominal (*Mass Shift*)** | Tidak mengisolasi dan menyimpan posisi koordinat referensi awal (*ground truth*) dari file backup sebelum melakukan edit. | **Wajib ekstraksi awal**: Baca koordinat $X_{right}$ dari `test_X.X.X_BACKUP_BEFORE_TAHAP7.xar` sebagai acuan mutlak sebelum edit. |
| **5** | **Angka 9 Berubah Menjadi Karakter Aneh / Rusak** | Karakter `9` pada encoding tertentu atau kerning individual offset corrupt. | Gunakan penulisan string UTF-16LE murni (`b'\x39\x00'`) dan perbarui payload string secara bersih via `XarDocument` DOM. |
| **6** | **Wrapping Teks Otomatis (Teks Bertingkat Dua Line)** | Karakter koma `,` atau spasi memicu pembagian kata (*word wrap*) pada container teks pendek. | Lakukan *unwrapping* (hilangkan line break / kerning Y vertikal) dan pastikan lebar container mencukupi. |

---

## III. RINGKASAN PROSEDUR STANDAR (TAHAP 1 HINGGA TAHAP 8)

### Tahap 1: Unifikasi & Pembersihan Struktur Teks
Ekstraksi string dari PDF/XAR dasar, pembersihan spasi ganda, unifikasi format tanggal, nominal, dan saldo.

### Tahap 2: Pengisian Data Transaksi Dinamis
Inject data transaksi baru (17 baris) ke dalam record XAR tanpa merusak indeks pointer internal.

### Tahap 3: Manajemen Warna Font (`Tag 150`)
Penerapan warna sesuai standar perbankan:
- Hijau (`#00A651` / `f0030000`) untuk Transaksi Masuk (`+`)
- Gelap/Hitam (`#333333` / `61020000`) untuk Transaksi Keluar (`-`)
- Biru (`#005B9C` / `4a040000`) untuk Saldo

### Tahap 4: Unwrapping & Proteksi Font Definition
Penghapusan line-break liar pada nama/keterangan transaksi dan proteksi ketat `Tag 2907` agar tidak memicu font reset.

### Tahap 5: Pembaruan Header & Footer Dokumentasi
Updating nomor rekening, periode, cabang, tanggal cetak (`Dicetak pada/Issued on`), dan nomor halaman (`Page 2 of 3` / `2 dari 3`).

### Tahap 6: Isolasi File Backup (*Pristine Backup Preservation*)
File `test_X.X.X_BACKUP_BEFORE_TAHAP7.xar` diisolasi sebagai acuan referensi asli yang tidak boleh diubah (*untouchable reference*).

### Tahap 7: Penguncian Matriks Rata Kanan Nominal
Penerapan formula $X_{left\_new} = X_{right\_nominal\_target} - (\text{Len} \times 0,177\text{ cm})$ pada seluruh 17 baris Nominal.

### Tahap 8 (STANDAR SOP UTAMA): Penguncian Koordinat Referensi Awal & Dual-Tag Rata Kanan Presisi (Nominal & Saldo)
1. **Ekstraksi Acuan**: Ekstrak $X_{right\_target}$ dari backup (Nominal: $15,08\text{ cm}$, Saldo: $19,47\text{ cm}$).
2. **Kalkulasi Dinamis**: Hitung $X_{left\_new}$ berdasarkan jumlah karakter baru.
3. **Pembaruan Berpasangan**: Synchronize `Tag 2100` (`TAG_MATRIX`) & `Tag 2206` (`TAG_TEXT_KERN_X_Y`).
4. **Dual Verification**: Verifikasi biner via DOM & verifikasi visual via Xara GUI dengan Ruler (`Ctrl + R`).

---

## IV. VERIFIKASI & METODE PENGUJIAN

SETIAP PERUBAHAN HARUS DIREVIEW DENGAN DUAL-STEP VERIFICATION:
1. **Biner DOM Verification Script**: Menjalankan script Python yang memvalidasi bahwa seluruh record `Tag 2100`, `Tag 2206`, dan `Tag 2208` mengembalikan status `100% OK`.
2. **GUI Ruler Verification**:
   * Tutup dokumen aktif di Xara Designer Pro+ (`Ctrl + W`).
   * Buka file `.xar` hasil update.
   * Tekan `Ctrl + R` (Show Rulers) untuk memastikan batas kanan angka Nominal mengunci di **$15,08\text{ cm} / 15,18\text{ cm}$** dan Saldo mengunci di **$19,47\text{ cm}$**.
