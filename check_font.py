import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")
for t in doc.get_transactions():
    if t["row"] == 1:
        ns = t["nom_story"]
        print("Nominal records:")
        for i in range(ns["story_idx"], ns["end_story_idx"]+1):
            r = doc.records[i]
            txt = ""
            if r["tag"] == 2201:
                txt = r["payload"].decode("utf-16le", errors="replace")
            print(f"  [{i}] Tag=0x{r['tag']:X} ({r['tag']}) size={r['size']} {txt}")
