import struct
from xar_dom_engine import XarDocument

input_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
output_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7_test.xar'

doc = XarDocument(input_file)
print(f"Loaded {len(doc.records)} records.")

GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

TARGET_XR_NOMINAL = 431320
TARGET_XR_SALDO = 570450

def update_entry(text_rec, new_text, t2206_rec, t2100_rec, target_xr, split_rec=None, color_rec=None, color_bytes=None):
    # 1. Update text
    r_txt = doc.records[text_rec]
    r_txt['payload'] = new_text.encode('utf-16le')
    r_txt['size'] = len(r_txt['payload'])
    
    # 2. Update split if present
    if split_rec:
        r_spl = doc.records[split_rec]
        r_spl['payload'] = "".encode('utf-16le')
        r_spl['size'] = len(r_spl['payload'])
        
    # 3. Calculate width
    w = calc_text_width(new_text)
    
    # 4. Update Tag 2206
    if t2206_rec:
        r_2206 = doc.records[t2206_rec]
        orig = struct.unpack('<iii', r_2206['payload'])
        r_2206['payload'] = struct.pack('<iii', w, orig[1], orig[2])
        r_2206['size'] = len(r_2206['payload'])
        
    # 5. Update Tag 2100
    if t2100_rec and target_xr:
        x_left = target_xr - w
        r_2100 = doc.records[t2100_rec]
        orig_2100 = struct.unpack('<iii', r_2100['payload'])
        r_2100['payload'] = struct.pack('<iii', x_left, orig_2100[1], orig_2100[2])
        r_2100['size'] = len(r_2100['payload'])
        
    # 6. Update Color if specified
    if color_rec and color_bytes:
        r_col = doc.records[color_rec]
        r_col['payload'] = color_bytes
        r_col['size'] = len(r_col['payload'])

# --- 1. HEADER SUMMARY ---
print("Updating Header Summary...")
# Dana Masuk: Rec 1275 -> '+ 5.315.920,00', split 1280 -> "", Tag 2206 Rec 1270 -> 55156, Color Rec 1271 -> Hijau
update_entry(1275, '+ 5.315.920,00', 1270, None, None, split_rec=1280, color_rec=1271, color_bytes=b'\x0b\x04\x00\x00')

# Dana Keluar: Rec 1292 -> '- 4.210.600,00 ', Tag 2206 Rec 1285 -> 57550, Color Rec 1286 -> Hitam
update_entry(1292, '- 4.210.600,00 ', 1285, None, None, color_rec=1286, color_bytes=b'\x76\x02\x00\x00')

# --- 2. TABLE ROWS (Rows 29 to 36) ---
print("Updating Table Rows 29 to 36...")

# Row 29
# Saldo: 3.264.003,00 (Rec 8336, Tag 2206: 8335, Tag 2100: 8319)
update_entry(8336, '3.264.003,00', 8335, 8319, TARGET_XR_SALDO)
# Nominal: +3.235.920,00 (Rec 8357, Tag 2206: 8356, Tag 2100: 8340, Color: 8345 Hijau)
update_entry(8357, '+3.235.920,00', 8356, 8340, TARGET_XR_NOMINAL, color_rec=8345, color_bytes=b'\x0b\x04\x00\x00')

# Row 30
# Saldo: 3.194.003,00 (Rec 8490, Tag 2206: 8489, Tag 2100: 8473)
update_entry(8490, '3.194.003,00', 8489, 8473, TARGET_XR_SALDO)

# Row 31
# Saldo: 3.193.503,00 (Rec 8663, Tag 2206: 8662, Tag 2100: 8646)
update_entry(8663, '3.193.503,00', 8662, 8646, TARGET_XR_SALDO)

# Row 32
# Saldo: 3.096.503,00 (Rec 8800, Tag 2206: 8799, Tag 2100: 8783)
update_entry(8800, '3.096.503,00', 8799, 8783, TARGET_XR_SALDO)
# Nominal: -97.000,00 (Rec 8821, Tag 2206: 8820, Tag 2100: 8804, Color: 8809 Hitam)
update_entry(8821, '-97.000,00', 8820, 8804, TARGET_XR_NOMINAL, color_rec=8809, color_bytes=b'\x95\x0e\x00\x00')

# Row 33
# Saldo: 3.096.003,00 (Rec 8907, Tag 2206: 8906, Tag 2100: 8890)
update_entry(8907, '3.096.003,00', 8906, 8890, TARGET_XR_SALDO)
# Nominal: -500,00 (Rec 8928, Tag 2206: 8927, Tag 2100: 8911, Color: 8916 Hitam)
update_entry(8928, '-500,00', 8927, 8911, TARGET_XR_NOMINAL, color_rec=8916, color_bytes=b'\x95\x0e\x00\x00')

# Row 34
# Saldo: 3.081.003,00 (Rec 9044, Tag 2206: 9043, Tag 2100: 9027)
update_entry(9044, '3.081.003,00', 9043, 9027, TARGET_XR_SALDO)
# Nominal: -15.000,00 (Rec 9065, Tag 2206: 9064, Tag 2100: 9048, Color: 9053 Hitam)
update_entry(9065, '-15.000,00', 9064, 9048, TARGET_XR_NOMINAL, color_rec=9053, color_bytes=b'\x95\x0e\x00\x00')

# Row 35
# Saldo: 2.981.003,00 (Rec 10189, Tag 2206: 10188, Tag 2100: 10172)
update_entry(10189, '2.981.003,00', 10188, 10172, TARGET_XR_SALDO)
# Nominal: -100.000,00 (Rec 10210, split 10215, Tag 2206: 10209, Tag 2100: 10193, Color: 10198 Hitam)
update_entry(10210, '-100.000,00', 10209, 10193, TARGET_XR_NOMINAL, split_rec=10215, color_rec=10198, color_bytes=b'\x95\x0e\x00\x00')

# Row 36
# Nominal: +300.000,00 (Rec 10367, split 10372, Tag 2206: 10366, Tag 2100: 10350, Color: 10355 Hijau)
update_entry(10367, '+300.000,00', 10366, 10350, TARGET_XR_NOMINAL, split_rec=10372, color_rec=10355, color_bytes=b'\x0b\x04\x00\x00')

# Save document
doc.save(output_file)
print(f"Saved: {output_file}")

# Verify
doc_v = XarDocument(output_file)
print(f"Verified records count: {len(doc_v.records)} (Expected: 14392)")
assert len(doc_v.records) == 14392

size_mismatches = [i for i, r in enumerate(doc_v.records) if len(r['payload']) != r['size']]
print(f"Size mismatches: {len(size_mismatches)}")
assert len(size_mismatches) == 0

print("\n--- ALL VERIFICATIONS PASSED! ---")
