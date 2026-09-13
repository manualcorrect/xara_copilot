from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")
for i in range(1015, 1038):
    r = doc.records[i]
    tag = r["tag"]
    sz = r["size"]
    pl = r["payload"]
    txt = ""
    if tag == 2201:
        txt = "STR: " + pl.decode("utf-16le", errors="replace")
    elif tag == 2202:
        txt = "CHAR: " + pl.decode("utf-16le", errors="replace")
    print(f"[{i}] Tag={tag} (0x{tag:X}) sz={sz} hex={pl.hex()} {txt}")
