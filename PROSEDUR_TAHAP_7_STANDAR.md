# 📜 PROSEDUR STANDAR TAHAP 7 & SISTEM PENANGANAN ERROR (SOP)

## 📌 1. DEFINISI & TUJUAN TAHAP 7
**Tahap 7** adalah tahap akhir dari proses penyuntingan laporan keuangan rekening koran (*e-Statement*) berbasis file biner Xara (`.xar`). 
Tujuan utamanya adalah memperbarui seluruh data keuangan secara presisi, konsisten, dan 100% bebas dari error visual maupun korupsi berkas biner.

---

## 🔄 2. SUB-PROSEDUR EKSEKUSI TAHAP 7

### A. Prosedur Tahap 7 Pertama (Single Row Alignment & Sample Test)
1. **Uji Coba Sampel**: Menguji pembaruan pada 1 baris transaksi sampel (misalnya Baris 2 `+1.500.000,00`) untuk memverifikasi keselarasan visual (pola rata kanan/*right-alignment*), lebar karakter, dan warna dasar.
2. **Validasi Grid Visual**: Memastikan teks nominal dan saldo mengikuti pola grid dan ruler Xara tanpa merusak kolom `Keterangan`.

### B. Prosedur Tahap 7 Kedua (Full Batch Automation & Story Unwrap)
1. **Eksekusi Batch Otomatis**: Memperbarui ke-17 baris transaksi (Halaman 1 dan Halaman 2) serta 4 *Header Summary Totals* (Saldo Awal, Dana Masuk, Dana Keluar, Saldo Akhir) secara simultan melalui `xar_dom_engine.py`.
2. **Intelligent Story Un-wrapping**: Mengosongkan seluruh record pecahan sekunder sisa template bawaan menggunakan mekanisme proteksi biner.

---

## 🛠️ 3. PROSEDUR BAKU PENANGANAN ERROR (ERROR RESOLUTION SOP)

### 🔴 Error 1: Berkas Rusak (`Failed to handle record 1722 2201`)
* **Penyebab**: Mengosongkan record teks pecahan sekunder dengan payload `0-byte` (`b""`). Parser biner Xara menganggap record `2201` berukuran 0 byte di dalam *Text Story* sebagai bentuk korupsi file.
* **Solusi Baku**:
  * Seluruh record pecahan sekunder WAJIB disuntikkan **Zero-Width Space (`\u200B` / `b'\x0b\x20'`)**.
  * Karakter 2-byte ini menjaga ukuran record tetap valid sehingga struktur *Text Story* Xara terbaca 100% utuh tanpa error.

### 🔴 Error 2: Angka Buntut / Fragmentasi Teks (`5.047.661,009`)
* **Penyebab**: Template asli Xara memecah angka ke dalam beberapa record `TAG_TEXT_CHAR` (2202) dan `TAG_TEXT_STRING` (2201). Mengganti teks utama tanpa meng-unwrap record sekunder menyebabkan Xara menyambung teks baru dengan angka sisa template.
* **Solusi Baku**:
  * Terapkan **Auto-Unwrap Story Biner** yang memetakan kontainer `TAG_TEXT_STORY_SIMPLE` (2200) hingga `TAG_TEXT_STORY_END` (2203).
  * Teks baru ditulis pada record utama (`matched_primary`), sedangkan SELURUH record `2201/2202` sekunder di dalam story tersebut di-unwrap menjadi `\u200B`.

### 🔴 Error 3: Font Berubah / Rusak (`PDF-PDF-PDF-PDF-PD`)
* **Penyebab**: Mengubah Tag `2907` atau menyapu record warna di luar kontainer objek nominal secara acak dapat merusak *Font Definition Nodes*, sehingga Xara mereset nama font ke font fallback (`PDF-PDF...`).
* **Solusi Baku**:
  * Tag `2907` (`b7010000`) adalah index acuan palet warna dan TIDAK BOLEH diubah pada node font.
  * Pembaruan warna HANYA dilakukan pada Record **Tag `150` (`TAG_WEBCOLOR`)** presisi milik objek nominal terkait:
    * 🟢 **Transaksi Kredit (`+`)**: Set Record Tag `150` ke **Hijau Mandiri (`f0030000` / `#00a651`)**.
    * ⬛ **Transaksi Debit (`-`)**: Set Record Tag `150` ke **Teks Gelap (`61020000` / `#333333`)**.

---

## 📋 4. VERIFIKASI DOM & KONTROL KUALITAS (CHECKLIST)

Setiap kali Tahap 7 dieksekusi, skrip verifikasi otomatis wajib memastikan:

1. **Text Matching**: 100% dari 17 Nominal dan 17 Saldo cocok persis dengan tabel keuangan ground truth.
2. **Summary Totals**: Saldo Awal, Dana Masuk (Hijau), Dana Keluar, dan Saldo Akhir 100% cocok secara matematis.
3. **Zero Residual Fragments**: Tidak ada karakter pecahan sisa (`9`, `00`, `100`, dll.) yang tertinggal.
4. **Color Integrity**: Transaksi Kredit (`+`) berwarna Hijau (`f0030000`) dan Debit (`-`) berwarna Gelap (`61020000`).
5. **Font Integrity**: Nama font tetap konsisten pada `TT Interphases Bold` / `TT Interphases Regular`.

---

> **Status Prosedur**: RESMI & TERINTEGRASI PADA SISTEM XARA COPILOT
