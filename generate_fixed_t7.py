from xar_dom_engine import XarDocument
import struct

input_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
output_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7_fixed.xar'

doc = XarDocument(input_file)
initial_count = len(doc.records)

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
    r_txt = doc.records[text_rec]
    r_txt['payload'] = new_text.encode('utf-16le')
    r_txt['size'] = len(r_txt['payload'])
    
    if split_rec:
        r_spl = doc.records[split_rec]
        # CRITICAL: Tag 2202 requires at least 2 bytes in UTF-16le (b'\x00\x00')
        r_spl['payload'] = b'\x00\x00'
        r_spl['size'] = len(r_spl['payload'])
        
    w = calc_text_width(new_text)
    
    if t2206_rec:
        r_2206 = doc.records[t2206_rec]
        orig = struct.unpack('<iii', r_2206['payload'])
        r_2206['payload'] = struct.pack('<iii', w, orig[1], orig[2])
        r_2206['size'] = len(r_2206['payload'])
        
    if t2100_rec and target_xr:
        x_left = target_xr - w
        r_2100 = doc.records[t2100_rec]
        orig_2100 = struct.unpack('<iii', r_2100['payload'])
        r_2100['payload'] = struct.pack('<iii', x_left, orig_2100[1], orig_2100[2])
        r_2100['size'] = len(r_2100['payload'])
        
    if color_rec and color_bytes:
        r_col = doc.records[color_rec]
        r_col['payload'] = color_bytes
        r_col['size'] = len(r_col['payload'])

# 1. Header Summary
update_entry(1275, '+ 5.315.920,00', 1270, None, None, split_rec=1280, color_rec=1271, color_bytes=b'\x0b\x04\x00\x00')
update_entry(1292, '- 4.210.600,00 ', 1285, None, None, color_rec=1286, color_bytes=b'\x76\x02\x00\x00')

# 2. Table Rows 29 to 36
update_entry(8336, '3.264.003,00', 8335, 8319, TARGET_XR_SALDO)
update_entry(8357, '+3.235.920,00', 8356, 8340, TARGET_XR_NOMINAL, color_rec=8345, color_bytes=b'\x0b\x04\x00\x00')
update_entry(8490, '3.194.003,00', 8489, 8473, TARGET_XR_SALDO)
update_entry(8663, '3.193.503,00', 8662, 8646, TARGET_XR_SALDO)
update_entry(8800, '3.096.503,00', 8799, 8783, TARGET_XR_SALDO)
update_entry(8821, '-97.000,00', 8820, 8804, TARGET_XR_NOMINAL, color_rec=8809, color_bytes=b'\x95\x0e\x00\x00')
update_entry(8907, '3.096.003,00', 8906, 8890, TARGET_XR_SALDO)
update_entry(8928, '-500,00', 8927, 8911, TARGET_XR_NOMINAL, color_rec=8916, color_bytes=b'\x95\x0e\x00\x00')
update_entry(9044, '3.081.003,00', 9043, 9027, TARGET_XR_SALDO)
update_entry(9065, '-15.000,00', 9064, 9048, TARGET_XR_NOMINAL, color_rec=9053, color_bytes=b'\x95\x0e\x00\x00')
update_entry(10189, '2.981.003,00', 10188, 10172, TARGET_XR_SALDO)
update_entry(10210, '-100.000,00', 10209, 10193, TARGET_XR_NOMINAL, split_rec=10215, color_rec=10198, color_bytes=b'\x95\x0e\x00\x00')
update_entry(10367, '+300.000,00', 10366, 10350, TARGET_XR_NOMINAL, split_rec=10372, color_rec=10355, color_bytes=b'\x0b\x04\x00\x00')

doc.save(output_file)
print("Saved:", output_file)

# Post-save checks
doc_v = XarDocument(output_file)
assert len(doc_v.records) == initial_count
assert len([i for i, r in enumerate(doc_v.records) if len(r['payload']) != r['size']]) == 0

# Check that NO record with Tag 2201 or 2202 has length 0!
zero_len_texts = [i for i, r in enumerate(doc_v.records) if r['tag'] in (2201, 2202) and len(r['payload']) == 0]
print("Zero length text records (must be 0):", len(zero_len_texts))
assert len(zero_len_texts) == 0

print("SUCCESS: test_3.1_tahap7_fixed.xar verified perfectly!")
