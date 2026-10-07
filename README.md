# Xara Co-Pilot Engine (Project V2)

Asisten otomasi presisi tinggi untuk pemrosesan, standarisasi, dan modifikasi dokumen biner **Xara Designer Pro+ (`.xar`)**, khususnya dokumen *e-Statement* / rekening koran perbankan (Bank Mandiri).

Sistem ini memanipulasi file biner `.xar` secara langsung pada tingkat DOM biner (Stream 5 DEFLATE, Tag Matrices, Kerning, Palet Warna, dan Unicode records) sehingga font native tetap konsisten visualnya meskipun font tersebut tidak terinstall di sistem operasi Windows.

---

## 📁 Struktur Direktori Repositori

```text
Xara_copilot/
├── jalankan_pipeline.bat        # Launcher batch Windows (otomatis / drag-and-drop Excel)
├── run_copilot_admin.bat        # Launcher mode Administrator
├── run_project_v2_pipeline.py   # Master Pipeline Runner (Tahap 1 - 7/8 otomatis)
├── xar_dom_engine.py            # Core Binary Parser & DOM Manipulation Engine
├── xara_bridge_service.py       # Win32 GUI Automation Bridge ke Xara Designer Pro+
├── smart_date_time_generator.py # Generator Tanggal & Jam Transaksi Cerdas
├── parse_excel_template.py      # Parser template spreadsheet masukan
├── xar_cli.py                   # Antarmuka Command-Line (CLI) inspeksi & update
├── Template_Pekerjaan_Xara.xlsx # Template Excel resmi input mutasi rekening
│
├── docs/                        # Dokumentasi SOP & Basis Pengetahuan
│   ├── PROJECT_V2_SOP.md        # Master SOP 7 Tahap Pengeditan Dokumen
│   ├── PROSEDUR_TAHAP_7_STANDAR.md # Standar Mutasi, Pewarnaan, & Saldo
│   └── KNOWLEDGE_BASE_XARA_PROCEDURES_AND_ERRORS.md # Solusi 40+ Kasus Error Biner Xara
│
├── data/                        # Dataset & File Pemetaan
│   ├── mappings/                # File JSON pemetaan baris, jadwal, & training history
│   └── dumps/                   # File teks log ekstraksi & dump baris transaksi
│
└── scripts/                     # Koleksi Skrip Pengujian & Utilitas Terstruktur
    ├── inspect/                 # 120+ skrip investigasi node & koordinat spesifik
    ├── verify/                  # 70+ skrip audit, verifikasi alignment & palet warna
    ├── tests/                   # Skrip unit test & pengujian engine
    └── archive/                 # Skrip tahapan transisi & eksperimen historis
```

---

## 🚀 Cara Menjalankan

### 1. Menjalankan Pipeline Otomatis (Rekomendasi)
Anda dapat langsung melakukan **drag-and-drop** file `Template_Pekerjaan_Xara.xlsx` (atau folder kerja yang berisi file `.xar`) ke file:
```cmd
jalankan_pipeline.bat
```
Atau jalankan melalui command line:
```bash
python run_project_v2_pipeline.py --excel "path\to\Template_Pekerjaan_Xara.xlsx"
```

### 2. Menggunakan CLI Cepat (`xar_cli.py`)
Melihat daftar transaksi dalam file `.xar`:
```bash
python xar_cli.py --file "dokumen.xar" --list
```
Mengubah baris transaksi tertentu:
```bash
python xar_cli.py --file "dokumen.xar" --row 1 --time "08:15:00 WIB" --nominal "+5.000.000,00"
```
Mengubah nama nasabah:
```bash
python xar_cli.py --file "dokumen.xar" --name "NAMA NASABAH"
```

---

## 📜 Alur Standar 7 Tahap (Master SOP)

Proses pengeditan dokumen dijalankan secara berurutan (*sequential*) untuk menjamin integritas biner:

1. **Tahap 1 - Perubahan Nama**: Pengubahan nama pemilik rekening (`Nama/Name`) dengan proteksi kerning & line break cabang.
2. **Tahap 2 - Perubahan Periode**: Pengubahan rentang tanggal laporan header pada seluruh halaman secara serentak.
3. **Tahap 3 - Perubahan Dicetak Pada**: Sinkronisasi tanggal penerbitan dokumen (*Issued on*).
4. **Tahap 4 - Perubahan Nomor Rekening**: Pengubahan nomor rekening dengan menjaga trailing space.
5. **Tahap 5 - Perubahan Nomor Halaman**: Sinkronisasi penomoran halaman header & footer (`Page X of Y` / `X dari Y`).
6. **Tahap 6 - Penyesuaian Tanggal & Jam**: Pengurutan kronologis, batas jam kerja bank (06:00 - 22:55 WIB), dan penguncian transaksi berjam kembar.
7. **Tahap 7 - Perubahan Finansial & Mutasi**: Pengubahan Saldo Awal, Dana Masuk (Hijau `#00A651`), Dana Keluar (Hitam `#000000`), Saldo Akhir (Biru `#005B9C`), dan perataan kanan (*ruler locking*).

Detail lengkap dapat dilihat di [docs/PROJECT_V2_SOP.md](file:///D:/X_Files/Antigravity/Xara_copilot/docs/PROJECT_V2_SOP.md).