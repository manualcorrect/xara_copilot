from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

# Fix Story at Y=405000:
for s in doc._get_stories():
    if s["y"] == 405000 and s["x"] != 123981:
        s_idx = s["story_idx"]
        print(f"Fixing story at Y=405000 (story_idx={s_idx})...")
        # Text: 'Transfer dari BANK MANDIRI'
        doc._set_record_unicode_string(s["string_indices"][0], "Transfer dari BANK MANDIRI")
        # Line width: 99816
        if s["line_indices"]:
            doc._set_line_width(s["line_indices"][0], 99816)
        doc._set_story_x(s_idx, 123981)

doc.save(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

# Verify
doc2 = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")
for s in doc2._get_stories():
    if s["y"] in (736000, 726000, 405000, 185000):
        print(f"Story [{s['story_idx']}] Y={s['y']} X={s['x']}: {repr(s['full_text'])}")
