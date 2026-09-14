from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== ALL DATE NODES IN 0.XAR ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Mar 2026' in txt:
            # find surrounding text
            prevs = [f"{k}:{doc.records[k]['payload'].decode('utf-16le', errors='ignore')}" for k in range(max(0, i-4), i) if doc.records[k]['tag'] in (2201, 2202)]
            print(f"[{i:5d}] Tag {r['tag']}: {txt!r:25s} | Prevs: {prevs}")
