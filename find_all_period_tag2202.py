from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)

print("=== CHECKING ALL PERIOD TAG 2202 NODES ===")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if '01 Jul 2026 - 31 Jul 2026' in txt:
            # Check previous 10 records for Tag 2202
            for j in range(max(0, i-10), i):
                if doc.records[j]['tag'] == 2202:
                    p_txt = doc.records[j]['payload'].decode('utf-16le', errors='ignore')
                    print(f"Page Period at Rec {i}: Found Tag 2202 at [{j}] with text: {p_txt!r} (payload: {doc.records[j]['payload'].hex()})")
