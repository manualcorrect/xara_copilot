from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

print("=" * 80)
print("INSPECTING ROW 1 AND ROW 2 NOMINAL NODES IN 0.XAR")
print("=" * 80)

print("\n--- Row 1 (Recs 1590 to 1640) ---")
for k in range(1590, 1640):
    r = doc.records[k]
    t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if r['tag'] in (2201, 2202) else ''
    print(f"Rec {k:5d} [Tag {r['tag']:4d}]: text='{t}' | hex={r['payload'].hex()[:20]}")

print("\n--- Row 2 (Recs 1750 to 1800) ---")
for k in range(1750, 1800):
    r = doc.records[k]
    t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00') if r['tag'] in (2201, 2202) else ''
    print(f"Rec {k:5d} [Tag {r['tag']:4d}]: text='{t}' | hex={r['payload'].hex()[:20]}")
