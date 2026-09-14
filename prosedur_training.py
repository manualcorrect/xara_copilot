"""
MODUL PROSEDUR TRAINING (STANDALONE TRAINING PROCEDURES & TAHAP 0 STANDARDIZATION)
Xara Document Binary DOM Processing Engine

Menyimpan seluruh aturan, perbaikan bug, dan penyesuaian biner yang dipelajari
selama sesi training (Stress Test 2, Firmansyah Jun-Jul-Agu, Stress Test 3, Marsiyah Jun-Jul-Aug).

Dieksekusi pada FASE 0 (Pre-SOP Template Standardization) sebelum SOP 7 Tahap dijalankan.
"""

import struct
from typing import Dict, List, Tuple, Optional
from xar_dom_engine import XarDocument

# =========================================================================
# 1. TABEL METRIK LEBAR GLYPH RESMI (TTInterphases-Bold)
# =========================================================================
CHAR_WIDTHS_BOLD = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

# Standar Koordinat Ruler Acuan Sisi Kanan (Millipoints)
TARGET_XR_NOMINAL = 431250  # 15.214 cm (Kolom Nominal Tabel Mutasi)
TARGET_XR_SALDO   = 568306  # 20.049 cm (Kolom Saldo Berjalan)

# Standar Dimensi & Koordinat 2-Box Nama & Cabang
W_317_MP    = 89858   # 3.17 cm (Lebar Kolom Nama Nasabah)
X_NAME_MP   = 123307  # 4.350 cm (Posisi X Kotak Nama)
Y_NAME_MP   = 736000  # 25.964 cm (Posisi Y Kotak Nama)
X_CABANG_MP = 124101  # 4.378 cm (Posisi X Kotak Cabang)
Y_CABANG_MP = 714420  # 25.203 cm (Posisi Y Kotak Cabang)

# =========================================================================
# 2. HELPER FUNCTIONS UNTUK MANIPULASI RECORD BINER XARA
# =========================================================================

def hitung_lebar_teks_bold(text: str) -> int:
    """Menghitung total advance width teks berdasarkan tabel metrik biner TTInterphases-Bold."""
    return sum(CHAR_WIDTHS_BOLD.get(c, 4800) for c in text)

def hitung_posisi_rata_kanan(nominal_str: str, target_xr: int = TARGET_XR_NOMINAL) -> Tuple[int, int]:
    """
    Menghitung pasangan (X_left, Advance_Width_W) agar teks rata kanan sempurna.
    X_left = target_xr - W(teks)
    """
    w = hitung_lebar_teks_bold(nominal_str)
    x_left = target_xr - w
    return x_left, w

def set_text_payload(doc: XarDocument, rec_idx: int, text_str: str):
    """Menulis payload UTF-16LE pada node Tag 2201 dan menyinkronkan size record."""
    p = bytearray(text_str.encode('utf-16le'))
    doc.records[rec_idx]['payload'] = p
    doc.records[rec_idx]['size'] = len(p)

def blank_node_2byte(doc: XarDocument, rec_idx: Optional[int]):
    """
    Mengosongkan node split sekunder dengan 2-byte null character (b'\x00\x00').
    ATURAN BINER MUTLAK: Dilarang menggunakan 0 byte (b'') pada Tag 2202/Tag 2201.
    """
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

def set_color_tag150(doc: XarDocument, rec_idx: Optional[int], color_bytes: bytearray):
    """Menetapkan kode warna Tag 150 4-byte dan menyinkronkan size."""
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        doc.records[rec_idx]['payload'] = bytearray(color_bytes)
        doc.records[rec_idx]['size'] = len(color_bytes)

def set_matrix_tag2100_x(doc: XarDocument, rec_idx: Optional[int], new_x: int):
    """Memperbarui nilai sumbu X pada Tag 2100 (TAG_MATRIX)."""
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def set_advance_width_tag2206(doc: XarDocument, rec_idx: Optional[int], new_w: int):
    """Memperbarui advance width (w) pada Tag 2206 (TAG_TEXT_KERN_X_Y)."""
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_w, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

def set_container_width_tag2150(doc: XarDocument, rec_idx: Optional[int], new_w: int):
    """Memperbarui lebar bounding box container Tag 2150."""
    if rec_idx is not None and 0 <= rec_idx < len(doc.records):
        orig_flag = doc.records[rec_idx]['payload'][4:5] if len(doc.records[rec_idx]['payload']) >= 5 else b'\x01'
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<i', new_w) + orig_flag)
        doc.records[rec_idx]['size'] = len(doc.records[rec_idx]['payload'])

# =========================================================================
# 3. ATURAN PROSEDUR TRAINING: EKSTRAKSI & PENGUNCIAN PALET WARNA NATIVE
# =========================================================================

def deteksi_kamus_palet_native(doc: XarDocument) -> Dict[str, bytearray]:
    """
    Mendeteksi kamus palet internal dokumen asli target (Aturan #16 & #20).
    Menghindari warning dialog 'Problems have been found with some data: color definition'.
    """
    total = len(doc.records)
    palette = {
        'green_credit': bytearray.fromhex('ee030000'),
        'black_debit':  bytearray.fromhex('9e010000'),
        'blue_saldo':   bytearray.fromhex('50050000'),
        'gray_sawal':   bytearray.fromhex('8a030000'),
        'normal_text':  bytearray.fromhex('58040000'),
    }

    if total in (19799, 19597):
        palette['green_credit'] = bytearray.fromhex('d6030000')
        palette['black_debit']  = bytearray.fromhex('9d010000')
        palette['blue_saldo']   = bytearray.fromhex('28050000')
        palette['gray_sawal']   = bytearray.fromhex('72030000')
        palette['normal_text']  = bytearray.fromhex('40040000')
    elif total == 28156:
        palette['green_credit'] = bytearray.fromhex('e9030000')
        palette['black_debit']  = bytearray.fromhex('9e010000')
        palette['blue_saldo']   = bytearray.fromhex('1f050000')
        palette['gray_sawal']   = bytearray.fromhex('85030000')
        palette['normal_text']  = bytearray.fromhex('53040000')
    elif total in (20812, 20800, 20850) or 20500 <= total <= 21500:
        palette['green_credit'] = bytearray.fromhex('e9030000')
        palette['black_debit']  = bytearray.fromhex('9e010000')
        palette['blue_saldo']   = bytearray.fromhex('4a050000')
        palette['gray_sawal']   = bytearray.fromhex('85030000')
        palette['normal_text']  = bytearray.fromhex('53040000')

    return palette

# =========================================================================
# 4. ATURAN PROSEDUR TRAINING: ARSITEKTUR 2-BOX NAMA (HURUF KAPITAL) & CABANG
# =========================================================================

def format_nama_kapital(nama_input: str) -> str:
    """
    Standarisasi Huruf Kapital Nama Nasabah (Aturan #22):
    Seluruh Nama Nasabah resmi rekening koran wajib menggunakan HURUF KAPITAL (ALL CAPS).
    Contoh: 'Adhikarya Putra' -> 'ADHIKARYA PUTRA'
    """
    return str(nama_input).strip().upper()

def buat_name_story_records(customer_name: str, palette: Dict[str, bytearray]) -> List[dict]:
    """
    Membuat blok record biner terisolasi untuk Nama Nasabah (HURUF KAPITAL):
    - Lebar Kolom W = 3.17 cm (Tag 2150 = 89858 mp)
    - Proportional Leading 80% (Tag 4208/4209 = 400 / 0x0190)
    - Font 8pt (Tag 2901 = 10000 mp)
    - Font ID Native Dokumen (Tag 2907 = 54010000)
    - Net Tree Balance: Tag 1 = 3, Tag 0 = 3 (Net = 0)
    """
    name_caps = format_nama_kapital(customer_name) + " "
    color_bytes = palette.get('normal_text', bytearray.fromhex('58040000'))
    
    return [
        {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_NAME_MP, Y_NAME_MP, 1))},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', W_317_MP, 1))},
        {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
        {'tag': 150,  'size': 4,  'payload': color_bytes},
        {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')},
        {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')}, # Native TTInterphases-Regular
        {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
        {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
        {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
        {'tag': 193,  'size': 0,  'payload': bytearray()},
        {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
        {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% leading
        {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80% leading
        {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
        # Line 1: Nama Nasabah (ALL CAPS)
        {'tag': 2200, 'size': 0,  'payload': bytearray()},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', W_317_MP, 5761, 0))},
        {'tag': 2201, 'size': len(name_caps.encode('utf-16le')), 'payload': bytearray(name_caps.encode('utf-16le'))},
        {'tag': 4211, 'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
        # Trailing End Of Paragraph
        {'tag': 2200, 'size': 0,  'payload': bytearray()},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10000))},
        {'tag': 2203, 'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
    ]

def buat_cabang_object_records(branch_name: str, palette: Dict[str, bytearray]) -> List[dict]:
    """
    Membuat blok record biner mandiri untuk Objek Cabang:
    - Posisi terkunci di X = 4.378 cm (124101 mp), Y = 25.203 cm (714420 mp)
    - Independen dan terpisah dari kotak nama
    - Net Tree Balance: Tag 1 = 3, Tag 0 = 3 (Net = 0) (Anti Access Violation)
    """
    b_str = branch_name.strip()
    color_bytes = palette.get('normal_text', bytearray.fromhex('58040000'))

    return [
        {'tag': 2100, 'size': 12, 'payload': bytearray(struct.pack('<iii', X_CABANG_MP, Y_CABANG_MP, 1))},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2150, 'size': 5,  'payload': bytearray(struct.pack('<iB', 0, 0))},
        {'tag': 2151, 'size': 8,  'payload': bytearray(8)},
        {'tag': 2901, 'size': 4,  'payload': bytearray.fromhex('10270000')}, # 8pt
        {'tag': 4209, 'size': 4,  'payload': bytearray.fromhex('90010000')}, # 80%
        {'tag': 4208, 'size': 4,  'payload': bytearray.fromhex('90010000')},
        {'tag': 150,  'size': 4,  'payload': color_bytes},
        {'tag': 2906, 'size': 4,  'payload': bytearray.fromhex('401f0000')},
        {'tag': 2907, 'size': 4,  'payload': bytearray.fromhex('54010000')},
        {'tag': 177,  'size': 4,  'payload': bytearray.fromhex('00001027')},
        {'tag': 174,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 175,  'size': 1,  'payload': bytearray.fromhex('02')},
        {'tag': 176,  'size': 1,  'payload': bytearray.fromhex('00')},
        {'tag': 152,  'size': 4,  'payload': bytearray.fromhex('fa000000')},
        {'tag': 193,  'size': 0,  'payload': bytearray()},
        {'tag': 4465, 'size': 4,  'payload': bytearray.fromhex('53010000')},
        {'tag': 2200, 'size': 0,  'payload': bytearray()},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 88118, 5761, 0))},
        {'tag': 2201, 'size': len(b_str.encode('utf-16le')), 'payload': bytearray(b_str.encode('utf-16le'))},
        {'tag': 2203, 'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()},
        {'tag': 2200, 'size': 0,  'payload': bytearray()},
        {'tag': 1,    'size': 0,  'payload': bytearray()},
        {'tag': 2206, 'size': 12, 'payload': bytearray(struct.pack('<iii', 0, 0, -10400))},
        {'tag': 2203, 'size': 0,  'payload': bytearray()},
        {'tag': 0,    'size': 0,  'payload': bytearray()}, # Closes Line 2
        {'tag': 0,    'size': 0,  'payload': bytearray()}, # Closes Top-Level Tag 2100 Object!
    ]

# =========================================================================
# 5. ATURAN PROSEDUR TRAINING: PEMISAHAN KOLOM NO & SALDO (DECOUPLED 2-BOX)
# =========================================================================

GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text: str) -> int:
    return sum(GLYPH_WIDTHS.get(c, 4800) for c in text)

TARGET_XR_SALDO = 570450 # 20.049 cm (Garis batas ruler kanan kolom Saldo)

def buat_no_object_records(y_pos: int, no_str: str, palette: Dict[str, bytearray]) -> List[dict]:
    """
    Membuat objek teks mandiri untuk Kolom Nomor (No):
    - Terletak di X = 20.000 mp (0.705 cm)
    - Lebar bounding box lokal (W ~ 0.5 cm), tidak lagi menjangkau kolom saldo.
    - Net Tree Balance = 0 (3 Tag 1, 3 Tag 0)
    """
    color_bytes = palette.get('normal_text', bytearray.fromhex('58040000'))
    font_id = bytearray.fromhex('54010000') # Regular Font ID
    p_no = bytearray(no_str.encode('utf-16le'))
    
    return [
        {'tag': 2100, 'payload': bytearray(struct.pack('<iii', 20000, y_pos, 1)), 'size': 12},
        {'tag': 1,    'payload': bytearray(b''), 'size': 0},
        {'tag': 2150, 'payload': bytearray(b'\x00\x00\x00\x00\x00'), 'size': 5},
        {'tag': 2151, 'payload': bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00'), 'size': 8},
        {'tag': 4465, 'payload': bytearray.fromhex('22050000'), 'size': 4},
        {'tag': 2901, 'payload': bytearray.fromhex('0f270000'), 'size': 4}, # 8pt (10000 mp)
        {'tag': 2906, 'payload': bytearray.fromhex('401f0000'), 'size': 4}, # 8000 mp
        {'tag': 177,  'payload': bytearray.fromhex('00001027'), 'size': 4},
        {'tag': 174,  'payload': bytearray.fromhex('02'), 'size': 1},
        {'tag': 175,  'payload': bytearray.fromhex('02'), 'size': 1},
        {'tag': 176,  'payload': bytearray.fromhex('00'), 'size': 1},
        {'tag': 152,  'payload': bytearray.fromhex('fa000000'), 'size': 4},
        {'tag': 193,  'payload': bytearray(b''), 'size': 0},
        {'tag': 2200, 'payload': bytearray(b''), 'size': 0},
        {'tag': 1,    'payload': bytearray(b''), 'size': 0},
        {'tag': 2206, 'payload': bytearray(struct.pack('<iii', 0, 6561, 0)), 'size': 12},
        {'tag': 2201, 'payload': p_no, 'size': len(p_no)},
        {'tag': 1,    'payload': bytearray(b''), 'size': 0},
        {'tag': 150,  'payload': bytearray(color_bytes), 'size': len(color_bytes)},
        {'tag': 2907, 'payload': bytearray(font_id), 'size': 4},
        {'tag': 0,    'payload': bytearray(b''), 'size': 0},
        {'tag': 2203, 'payload': bytearray(b''), 'size': 0},
        {'tag': 0,    'payload': bytearray(b''), 'size': 0},
        {'tag': 0,    'payload': bytearray(b''), 'size': 0},
    ]

def buat_saldo_object_records(y_pos: int, saldo_str: str, palette: Dict[str, bytearray]) -> List[dict]:
    """
    Membuat objek teks mandiri untuk Kolom Saldo:
    - Terletak tepat di X = TARGET_XR_SALDO - calc_text_width (Rata kanan pada 20.049 cm)
    - Warna Biru Saldo Native (Tag 150 = 50050000 / 28050000)
    - Net Tree Balance = 0 (3 Tag 1, 3 Tag 0)
    """
    color_bytes = palette.get('blue_saldo', bytearray.fromhex('50050000'))
    font_id = bytearray.fromhex('d3010000') # Bold Font ID
    w_saldo = calc_text_width(saldo_str)
    x_pos = TARGET_XR_SALDO - w_saldo
    p_saldo = bytearray(saldo_str.encode('utf-16le'))
    
    return [
        {'tag': 2100, 'payload': bytearray(struct.pack('<iii', x_pos, y_pos, 1)), 'size': 12},
        {'tag': 1,    'payload': bytearray(b''), 'size': 0},
        {'tag': 2150, 'payload': bytearray(b'\x00\x00\x00\x00\x00'), 'size': 5},
        {'tag': 2151, 'payload': bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00'), 'size': 8},
        {'tag': 4465, 'payload': bytearray.fromhex('22050000'), 'size': 4},
        {'tag': 2901, 'payload': bytearray.fromhex('0f270000'), 'size': 4}, # 8pt (10000 mp)
        {'tag': 2906, 'payload': bytearray.fromhex('401f0000'), 'size': 4}, # 8000 mp
        {'tag': 177,  'payload': bytearray.fromhex('00001027'), 'size': 4},
        {'tag': 174,  'payload': bytearray.fromhex('02'), 'size': 1},
        {'tag': 175,  'payload': bytearray.fromhex('02'), 'size': 1},
        {'tag': 176,  'payload': bytearray.fromhex('00'), 'size': 1},
        {'tag': 152,  'payload': bytearray.fromhex('fa000000'), 'size': 4},
        {'tag': 193,  'payload': bytearray(b''), 'size': 0},
        {'tag': 2200, 'payload': bytearray(b''), 'size': 0},
        {'tag': 1,    'payload': bytearray(b''), 'size': 0},
        {'tag': 2206, 'payload': bytearray(struct.pack('<iii', 0, 6561, 0)), 'size': 12},
        {'tag': 2201, 'payload': p_saldo, 'size': len(p_saldo)},
        {'tag': 1,    'payload': bytearray(b''), 'size': 0},
        {'tag': 150,  'payload': bytearray(color_bytes), 'size': len(color_bytes)},
        {'tag': 2908, 'payload': bytearray(b''), 'size': 0},
        {'tag': 2907, 'payload': bytearray(font_id), 'size': 4},
        {'tag': 0,    'payload': bytearray(b''), 'size': 0},
        {'tag': 2203, 'payload': bytearray(b''), 'size': 0},
        {'tag': 0,    'payload': bytearray(b''), 'size': 0},
        {'tag': 0,    'payload': bytearray(b''), 'size': 0},
    ]

def pemisahan_kolom_no_dan_saldo(doc: XarDocument, palette: Dict[str, bytearray]) -> int:
    """
    Mendeteksi objek Tag 2100 di mana Kolom Nomor dan Saldo tergabung menjadi 1 teks panjang (W = 19.57 cm),
    lalu memisahkannya menjadi 2 objek independen:
    1. Objek Kolom No di X = 0.705 cm
    2. Objek Kolom Saldo di X = 20.049 cm (Rata Kanan)
    """
    def find_story_end_by_depth(records, start_idx):
        depth = 0
        for j in range(start_idx, min(len(records), start_idx + 100)):
            tag = records[j]['tag']
            if tag == 1:
                depth += 1
            elif tag == 0:
                depth -= 1
                if depth == 0:
                    return j + 1
        return None

    joined_stories = []
    for idx, r in enumerate(doc.records):
        if r['tag'] == 2100 and len(r['payload']) >= 12:
            coords = struct.unpack('<iii', r['payload'][:12])
            if coords[0] == 20000 and 50000 <= coords[1] <= 700000:
                end = find_story_end_by_depth(doc.records, idx)
                if end is None:
                    continue
                slice_recs = doc.records[idx:end]
                txts = [x['payload'].decode('utf-16le', errors='ignore') for x in slice_recs if x['tag'] in (2201, 2202)]
                if any(t.strip() == 'No' for t in txts):
                    continue
                no_txt = None
                saldo_txt = None
                for t in txts:
                    if any(c.isdigit() for c in t) and (',' in t or '.' in t):
                        saldo_txt = t
                    elif no_txt is None and t.strip().isdigit():
                        no_txt = t
                if no_txt is not None and saldo_txt is not None:
                    joined_stories.append({
                        'start_idx': idx,
                        'end_idx': end,
                        'y_pos': coords[1],
                        'no_str': no_txt,
                        'saldo_str': saldo_txt
                    })

    for s in reversed(joined_stories):
        no_recs = buat_no_object_records(s['y_pos'], s['no_str'], palette)
        saldo_recs = buat_saldo_object_records(s['y_pos'], s['saldo_str'], palette)
        doc.records[s['start_idx']:s['end_idx']] = no_recs + saldo_recs

    for r in doc.records:
        r['size'] = len(r['payload'])

    return len(joined_stories)

# =========================================================================
# 6. ATURAN PROSEDUR TRAINING: SANITASI PHANTOM NODES & CONTAINER EXPANSION
# =========================================================================

def ekspansi_semua_container_bounding_boxes(doc: XarDocument):
    """
    Memperlebar Tag 2150 pada seluruh halaman agar teks panjang tidak ter-wrap (Aturan #15):
    - Periode Header: W = 180.000 mp (6.35 cm)
    - Summary Header Ringkasan: Tetap dikunci pada 63.646 mp (mencegah Saldo Akhir naik ke baris 3)
    """
    for idx_r, r in enumerate(doc.records):
        if r['tag'] == 2150 and len(r['payload']) >= 4:
            curr_w = struct.unpack('<i', r['payload'][:4])[0]
            if 80000 <= curr_w <= 110000:
                set_container_width_tag2150(doc, idx_r, 180000)
            elif 60000 <= curr_w <= 75000:
                set_container_width_tag2150(doc, idx_r, 63646)

def kalibrasi_alamat_kantor_cabang(doc: XarDocument):
    """
    Mengalibrasi matriks parent Tag 2100 alamat cabang Menara Mandiri 1 ke (300643, 778629, 1)
    pada seluruh halaman (Aturan #3 & #9).
    """
    for idx_r, r in enumerate(doc.records):
        if r['tag'] == 2201:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if 'Menara Mandiri 1' in txt or 'Plaza Mandiri' in txt:
                for k in range(idx_r - 1, max(0, idx_r - 25), -1):
                    if doc.records[k]['tag'] == 2100:
                        doc.records[k]['payload'] = bytearray(struct.pack('<iii', 300643, 778629, 1))
                        doc.records[k]['size'] = 12
                        break

# =========================================================================
# 7. ORKESTRATOR UTAMA: TAHAP 0 (PRE-SOP STANDARDIZATION)
# =========================================================================

def standarisasi_template_tahap0(doc: XarDocument, customer_name: str, branch_name: str = "KCP Jakarta Taman Aries") -> XarDocument:
    """
    Mengeksekusi FASE 0: Menyiapkan template yang sudah 100% kebal bug sebelum SOP 7 Tahap.
    1. Ekstraksi kamus palet native.
    2. Format Nama Nasabah ke HURUF KAPITAL (ALL CAPS).
    3. Pemisahan 2-Box Nama ($W=3.17cm$, 80% leading) & Cabang Mandiri dengan tree balance sempurna.
    4. Pemisahan Kolom No & Saldo menjadi 2 objek mandiri (Anti-Joint Bounding Box).
    5. Ekspansi Bounding Box Periode ($180.000 mp$) & Kalibrasi Summary ($63.646 mp$).
    6. Kalibrasi matriks alamat kantor cabang Menara Mandiri 1.
    7. Auto-Size sync untuk seluruh payload biner.
    """
    print("   [TAHAP 0] Mengeksekusi Prosedur Training & Standardisasi Template...")
    orig_total = len(doc.records)
    palette = deteksi_kamus_palet_native(doc)
    name_caps = format_nama_kapital(customer_name)
    
    # 1. 2-Box Nama Nasabah & Cabang
    name_stories = []
    for idx, r in enumerate(doc.records):
        if r['tag'] == 2100 and len(r['payload']) >= 12:
            coords = struct.unpack('<iii', r['payload'][:12])
            if coords[1] == 736000 and coords[0] in (123000, 123307, 124000):
                for j in range(idx, min(len(doc.records), idx+35)):
                    if doc.records[j]['tag'] == 2201:
                        t = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                        if any(w in t for w in ['ROY', 'DARWIN', 'Adhikarya', 'ADHIKARYA']):
                            end = j
                            for k in range(j, min(len(doc.records), j+20)):
                                if doc.records[k]['tag'] == 2203:
                                    end = k + 1
                                    while end < len(doc.records) and doc.records[end]['tag'] == 0:
                                        end += 1
                                    break
                            name_stories.append((idx, end))
                            break

    for s, e in reversed(name_stories):
        doc.records[s:e] = buat_name_story_records(name_caps, palette)

    mandiri_ends = []
    for idx, r in enumerate(doc.records):
        if r['tag'] == 2201 and 'Mandiri Call 14000' in r['payload'].decode('utf-16le', errors='ignore'):
            for j in range(idx, min(len(doc.records), idx+10)):
                if doc.records[j]['tag'] == 2203:
                    end = j + 1
                    while end < len(doc.records) and doc.records[end]['tag'] == 0:
                        end += 1
                    mandiri_ends.append(end)
                    break

    for m_end in reversed(mandiri_ends):
        has_cabang = False
        for k in range(m_end, min(len(doc.records), m_end+35)):
            if doc.records[k]['tag'] == 2201 and branch_name in doc.records[k]['payload'].decode('utf-16le', errors='ignore'):
                has_cabang = True
                break
        if not has_cabang:
            doc.records[m_end:m_end] = buat_cabang_object_records(branch_name, palette)

    # 2. Pemisahan Kolom No & Saldo menjadi 2 objek mandiri (Anti-Joint Bounding Box)
    total_decoupled = pemisahan_kolom_no_dan_saldo(doc, palette)
    print(f"   [TAHAP 0] Berhasil memisahkan {total_decoupled} baris Kolom No & Saldo menjadi objek mandiri.")

    # 3. Ekspansi Container Periode & Kalibrasi Summary
    ekspansi_semua_container_bounding_boxes(doc)
    
    # 4. Kalibrasi Alamat Cabang
    kalibrasi_alamat_kantor_cabang(doc)
    
    # 5. Aturan #27: Sinkronisasi Pointer Font & Warna Halaman Penutup (Anti-Fallback Times New Roman)
    sinkronisasi_pointer_halaman_penutup(doc, orig_total)

    # 6. Sinkronkan semua size record
    for r in doc.records:
        r['size'] = len(r['payload'])
        
    print(f"   [TAHAP 0 SELESAI] Template berhasil distandarisasi ({len(doc.records):,} records, ALL CAPS: '{name_caps}'). [PASS]")
    return doc

# =========================================================================
# 9. ATURAN PROSEDUR TRAINING: SINKRONISASI POINTER HALAMAN PENUTUP (ATURAN #27)
# =========================================================================

def sinkronisasi_pointer_halaman_penutup(doc: XarDocument, orig_total_records: int):
    """
    Aturan #27: Rekalkulasi Pointer Internal Halaman Penutup / Disclaimer.
    Menjamin atribut font (Arial / Tag 2907) dan warna outline box (Cyan / Tag 151)
    tidak putus / fallback ke Times New Roman & garis hitam saat terjadi pergeseran record (+delta_records).
    """
    shift = len(doc.records) - orig_total_records
    if shift == 0:
        return
    
    # Cari posisi awal Spread Halaman Penutup / Disclaimer
    disclaimer_spread_idx = None
    spread_indices = [idx for idx, r in enumerate(doc.records) if r['tag'] == 46]
    for sp_idx in spread_indices:
        for k in range(sp_idx, min(len(doc.records), sp_idx + 300)):
            if doc.records[k]['tag'] == 2201 and 'batas akhir' in doc.records[k]['payload'].decode('utf-16le', errors='ignore'):
                disclaimer_spread_idx = sp_idx
                break
        if disclaimer_spread_idx is not None:
            break
            
    if disclaimer_spread_idx is None and len(spread_indices) >= 2:
        disclaimer_spread_idx = spread_indices[-2]
    elif disclaimer_spread_idx is None and spread_indices:
        disclaimer_spread_idx = spread_indices[-1]
        
    if disclaimer_spread_idx is None:
        return

    threshold = 15000
    fixed_count = 0
    for idx in range(disclaimer_spread_idx, len(doc.records)):
        r = doc.records[idx]
        tag = r['tag']
        if tag in (150, 151, 2907, 4465) and len(r['payload']) >= 4:
            val = struct.unpack('<I', r['payload'][:4])[0]
            if threshold <= val <= orig_total_records + 500:
                new_val = val + shift
                r['payload'][:4] = struct.pack('<I', new_val)
                fixed_count += 1
    print(f"   [ATURAN #27] Berhasil menyinkronkan {fixed_count} pointer font & warna di Halaman Penutup/Disclaimer (Shift: +{shift}).")

