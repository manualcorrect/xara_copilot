from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

print("=" * 80)
print("MAPPING ALL DATE AND TIME NODES IN 0.XAR")
print("=" * 80)

date_nodes = []
time_nodes = []

for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if 'Feb 2026' in t and len(t) >= 10 and not any(w in t for w in ['-', 'Period', 'Periode']):
            date_nodes.append((i, t))
        elif 'WIB' in t or (len(t) >= 8 and t.count(':') == 2 and any(c.isdigit() for c in t)):
            time_nodes.append((i, t))

print(f"Total Date nodes found: {len(date_nodes)}")
print(f"Total Time nodes found: {len(time_nodes)}")

for i in range(min(15, len(date_nodes))):
    print(f"Row {i+1:2d} | Date Rec {date_nodes[i][0]:5d}: '{date_nodes[i][1]}' | Time Rec {time_nodes[i][0]:5d}: '{time_nodes[i][1]}'")
