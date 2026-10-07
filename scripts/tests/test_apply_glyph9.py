import sys
import os
import json
import struct
from xar_dom_engine import XarDocument

# 1. Extract glyph '9' from test_3.1.xar
doc3 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
glyph_9_rec = None
for r in doc3.records:
    if r['tag'] == 4350 and len(r['payload']) >= 6:
        fid = int.from_bytes(r['payload'][:4], 'little')
        cc = int.from_bytes(r['payload'][4:6], 'little')
        if fid == 13 and cc == 57: # '9'
            glyph_9_rec = {
                'tag': r['tag'],
                'size': len(r['payload']),
                'payload': bytearray(r['payload'])
            }
            break

assert glyph_9_rec is not None, "Glyph 9 not found in test_3.1.xar!"
print(f"Extracted glyph 9: tag={glyph_9_rec['tag']}, len={len(glyph_9_rec['payload'])}")

# 2. Test inserting into a copy of current test_v2.1_tahap7.xar
v2_in = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar'
v2_test_out = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7_with_glyph9.xar'

doc = XarDocument(v2_in)
print(f"Current doc records count: {len(doc.records)}")

# Find glyph 8 in font 13
idx_8 = None
for i, r in enumerate(doc.records):
    if r['tag'] == 4350 and len(r['payload']) >= 6:
        fid = int.from_bytes(r['payload'][:4], 'little')
        cc = int.from_bytes(r['payload'][4:6], 'little')
        if fid == 13 and cc == 56: # '8'
            idx_8 = i
            break

assert idx_8 is not None, "Glyph 8 not found in doc!"
print(f"Found glyph 8 at index {idx_8}")

# Insert glyph 9 right after glyph 8
doc.records.insert(idx_8 + 1, glyph_9_rec)
print(f"Inserted glyph 9 at index {idx_8 + 1}, new record count: {len(doc.records)}")

# Verify all records size sync
for r in doc.records:
    r['size'] = len(r['payload'])

doc.save(v2_test_out)
print(f"Saved successfully to: {v2_test_out}")
