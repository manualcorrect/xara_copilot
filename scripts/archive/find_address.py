from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

print("Searching for 'Plaza' in doc.records...")
for i, r in enumerate(doc.records):
    txt = ""
    if r["tag"] == 2201:
        txt = r["payload"].decode("utf-16le", errors="replace")
    elif r["tag"] == 2200:
        txt = r["payload"].decode("latin1", errors="replace")
    if "plaza" in txt.lower() or "gatot" in txt.lower() or "subroto" in txt.lower():
        print(f"Rec [{i}] Tag=0x{r['tag']:X} ({r['tag']}) size={r['size']}: {repr(txt)}")
        # Look backwards for Tag 2100 (Story position) and Tag 2206 (Line metrics)
        for k in range(i - 1, max(0, i - 25), -1):
            if doc.records[k]["tag"] == 2100:
                ints = struct.unpack(f"<{len(doc.records[k]['payload'])//4}i", doc.records[k]['payload'][:(len(doc.records[k]['payload'])//4)*4])
                print(f"   Enclosing Story [{k}] coords={ints} (X={ints[0]} mp = {ints[0]/28346.4567:.3f} cm)")
                break
