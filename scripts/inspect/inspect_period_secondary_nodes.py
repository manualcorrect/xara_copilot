from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

period_recs = [1028, 3673, 6457, 9181, 11901, 14677, 17420, 20220]

print("=" * 80)
print("INSPECTING PERIOD NODES ACROSS ALL 8 PAGES")
print("=" * 80)

for p_idx, r_idx in enumerate(period_recs, 1):
    print(f"\n--- Page {p_idx} (around rec {r_idx}) ---")
    for k in range(r_idx - 6, r_idx + 8):
        r = doc.records[k]
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if r['tag'] in (2201, 2202) else ''
        print(f"  Rec {k:5d} [Tag {r['tag']:4d}]: text='{t}' | size={r['size']}")
