import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

# Let's collect all (string, width) pairs from Nominal and Balance stories
samples = []
for t in doc.get_transactions():
    for story_key in ("nom_story", "bal_story"):
        s = t[story_key]
        if s and s["line_indices"] and s["string_indices"]:
            txt = doc.records[s["string_indices"][0]]["payload"].decode("utf-16le")
            w = struct.unpack("<i", doc.records[s["line_indices"][0]]["payload"][:4])[0]
            samples.append((txt, w))

print("Samples (text, width in millipoints):")
for txt, w in samples:
    print(f"  {txt:15s} : {w}")
