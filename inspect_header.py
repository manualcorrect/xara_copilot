from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")
stories = doc._get_stories()

print("Header stories (Y >= 600000):")
for s in sorted(stories, key=lambda x: (-x["y"], x["x"])):
    if s["y"] >= 600000 and s["full_text"]:
        print(f"Y={s['y']:6d} | X={s['x']:6d} | Story [{s['story_idx']}] : {repr(s['full_text'])}")
