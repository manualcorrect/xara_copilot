from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

print("=== Inspecting Story [1101] ('1 of 7') ===")
for i in range(1101, 1126):
    r = doc.records[i]
    txt = ""
    tag = r["tag"]
    sz = r["size"]
    pl = r["payload"]
    if tag == 2201:
        txt = "STR: " + pl.decode("utf-16le", errors="replace")
    elif tag == 2202:
        txt = "CHAR: " + pl.decode("utf-16le", errors="replace")
    elif tag == 2206:
        ints = struct.unpack(f"<{len(pl)//4}i", pl[:(len(pl)//4)*4])
        txt = f"LINE COORDS: {ints}"
    elif tag == 2100:
        ints = struct.unpack(f"<{len(pl)//4}i", pl[:(len(pl)//4)*4])
        txt = f"STORY COORDS: {ints}"
    print(f"[{i:4d}] Tag=0x{tag:04X} ({tag:4d}) sz={sz:2d} {txt}")

print("\n=== Inspecting Story [1216] ('1 dari 7') ===")
for i in range(1216, 1236):
    r = doc.records[i]
    txt = ""
    tag = r["tag"]
    sz = r["size"]
    pl = r["payload"]
    if tag == 2201:
        txt = "STR: " + pl.decode("utf-16le", errors="replace")
    elif tag == 2202:
        txt = "CHAR: " + pl.decode("utf-16le", errors="replace")
    elif tag == 2206:
        ints = struct.unpack(f"<{len(pl)//4}i", pl[:(len(pl)//4)*4])
        txt = f"LINE COORDS: {ints}"
    elif tag == 2100:
        ints = struct.unpack(f"<{len(pl)//4}i", pl[:(len(pl)//4)*4])
        txt = f"STORY COORDS: {ints}"
    print(f"[{i:4d}] Tag=0x{tag:04X} ({tag:4d}) sz={sz:2d} {txt}")
