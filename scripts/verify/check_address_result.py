from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")
for i in range(306, 315):
    r = doc.records[i]
    tag = r["tag"]
    sz = r["size"]
    pl = r["payload"]
    txt = ""
    if tag == 2201:
        txt = "STR: " + repr(pl.decode("utf-16le", errors="replace"))
    elif tag == 2206:
        txt = "LINE"
    elif tag == 2100:
        txt = "STORY"
    print(f"[{i:3d}] Tag=0x{tag:04X} ({tag:4d}) sz={sz:2d} hex={pl.hex()} {txt}")
