from xar_dom_engine import XarDocument
import struct

file_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
doc = XarDocument(file_path)

print("=== SEBELUM UPDATE HALAMAN ===")
# Story [1216]: '1 dari 7'
s_id = doc.records[1232]["payload"].decode("utf-16le")
# Story [1101]: '1 ' and 'of 7'
s_en1 = doc.records[1117]["payload"].decode("utf-16le")
s_en2 = doc.records[1122]["payload"].decode("utf-16le")
print(f"  Bahasa Indonesia : '{s_id}' (Story 1216, X={struct.unpack('<i', doc.records[1216]['payload'][:4])[0]})")
print(f"  Bahasa Inggris   : '{s_en1}{s_en2}' (Story 1101, X={struct.unpack('<i', doc.records[1101]['payload'][:4])[0]})")

# 1. Update Story [1216] ('1 dari 7' -> '2 dari 10')
NEW_PAGE_ID = "2 dari 10"
doc._set_record_unicode_string(1232, NEW_PAGE_ID)

# Right anchor for Story 1216
old_x_id = struct.unpack('<i', doc.records[1216]['payload'][:4])[0]
old_w_id = struct.unpack('<i', doc.records[1231]['payload'][:4])[0]
right_anchor_id = old_x_id + old_w_id # 559418

# Extra digit width ~ 3500 millipoints
new_w_id = old_w_id + 3500 # ~28638
doc._set_line_width(1231, new_w_id)
new_x_id = right_anchor_id - new_w_id
doc._set_story_x(1216, new_x_id)

# 2. Update Story [1101] ('1 of 7' -> '2 of 10')
doc._set_record_unicode_string(1117, "2 ")
doc._set_record_unicode_string(1122, "of 10")

# Right anchor for Story 1101
old_x_en = struct.unpack('<i', doc.records[1101]['payload'][:4])[0]
old_w_en = struct.unpack('<i', doc.records[1116]['payload'][:4])[0]
right_anchor_en = old_x_en + old_w_en # 559401

new_w_en = old_w_en + 3500 # ~20561
doc._set_line_width(1116, new_w_en)
new_x_en = right_anchor_en - new_w_en
doc._set_story_x(1101, new_x_en)

# Save document
doc.save(file_path)

# Verify reloaded from disk
doc_verify = XarDocument(file_path)
v_id = doc_verify.records[1232]["payload"].decode("utf-16le")
v_en1 = doc_verify.records[1117]["payload"].decode("utf-16le")
v_en2 = doc_verify.records[1122]["payload"].decode("utf-16le")

vx_id = struct.unpack('<i', doc_verify.records[1216]['payload'][:4])[0]
vw_id = struct.unpack('<i', doc_verify.records[1231]['payload'][:4])[0]

vx_en = struct.unpack('<i', doc_verify.records[1101]['payload'][:4])[0]
vw_en = struct.unpack('<i', doc_verify.records[1116]['payload'][:4])[0]

print("\n=== SESUDAH UPDATE HALAMAN (VERIFIKASI RELOAD DARI DISK) ===")
print(f"  Bahasa Indonesia : '{v_id}' (X={vx_id}, Right={vx_id + vw_id})")
print(f"  Bahasa Inggris   : '{v_en1}{v_en2}' (X={vx_en}, Right={vx_en + vw_en})")
