from xar_dom_engine import XarDocument

for name, path in [
    ('test_3.1.xar', r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar'),
    ('test_v2.1_tahap7.xar', r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')
]:
    doc = XarDocument(path)
    print(f"=== {name} (total {len(doc.records)} records) ===")
    for i, r in enumerate(doc.records):
        # Look for font strings in ASCII or UTF-16
        for b in [b"Arial", b"Helvetica", b"Calibri", b"Mandiri", b"Roboto", b"Segoe", b"PDF", b"Interphases", b"TT"]:
            if b in r["payload"] or b.lower() in r["payload"].lower():
                print(f"  Rec [{i}] Tag={r['tag']} (0x{r['tag']:X}) size={r['size']}: {r['payload'][:80]}")
                break
