from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

# Story 194:
# 1. Update Story position X to 10.63 cm = 301323 millipoints
NEW_X_CM = 10.63
NEW_X_MP = round(NEW_X_CM * 72000 / 2.54) # 301323
print(f"Setting Story [194] X from {struct.unpack('<i', doc.records[194]['payload'][:4])[0]} to {NEW_X_MP} ({NEW_X_CM} cm)")
doc._set_story_x(194, NEW_X_MP)

# 2. Update text in record 308
NEW_TEXT = "Menara Mandiri 1 Jalan Jenderal Sudirman Kav. 54-55, Jakarta 12190, Indonesia"
doc._set_record_unicode_string(308, NEW_TEXT)

# 3. Update line width in record 307
NEW_W = 270000 # ~9.52 cm
doc._set_line_width(307, NEW_W)

# 4. Remove the remaining split kern/string records [309:324]
# (records 309 to 323 inclusive: 15 records)
del doc.records[309:324]
print(f"Removed 15 orphan kern/split records [309:324]")

# Save
out_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
doc.save(out_path)

# Verify reloaded
doc_verify = XarDocument(out_path)
for s in doc_verify._get_stories():
    if s["story_idx"] == 194 or "menara" in s["full_text"].lower():
        x_mp = struct.unpack('<i', doc_verify.records[s['story_idx']]['payload'][:4])[0]
        y_mp = struct.unpack('<i', doc_verify.records[s['story_idx']]['payload'][4:8])[0]
        print(f"\n[VERIFIKASI RELOAD DARI DISK]:")
        print(f"  Story Index: {s['story_idx']}")
        print(f"  Posisi X   : {x_mp} millipoints ({x_mp * 2.54 / 72000:.2f} cm)")
        print(f"  Posisi Y   : {y_mp} millipoints ({y_mp * 2.54 / 72000:.2f} cm)")
        print(f"  Teks       : {repr(s['full_text'])}")
