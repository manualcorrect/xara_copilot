from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")
for s in doc._get_stories():
    if s["story_idx"] in (1101, 1216, 1732, 2606) or "dari" in s["full_text"].lower():
        print(f"Story [{s['story_idx']}] Y={s['y']} X={s['x']}: {repr(s['full_text'])}")
