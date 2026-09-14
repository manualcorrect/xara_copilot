import struct
from xar_dom_engine import XarDocument

target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
doc = XarDocument(target_xar)
print(f"Total records in 0_tahap7.xar: {len(doc.records):,}")

print("\n=== PERIOD RECORDS ACROSS ALL PAGES ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Jul 2026' in txt or 'Periode' in txt or 'Period' in txt:
            print(f"Record [{i}] Tag {r['tag']}: {txt!r}")
            # print surrounding 5 records
            for j in range(max(0, i-4), min(len(doc.records), i+5)):
                rec = doc.records[j]
                info = ""
                if rec['tag'] in (2201, 2202):
                    info = " | text: " + repr(rec['payload'].decode('utf-16le', errors='ignore'))
                elif rec['tag'] == 2100:
                    coords = struct.unpack(f'<{len(rec["payload"])//4}i', rec['payload'])
                    info = f" | coords: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)"
                print(f"   [{j}] Tag {rec['tag']} (sz {rec['size']}): {rec['payload'].hex()[:30]}{info}")
            print("-" * 50)

print("\n=== PAGE 1 NAME & CABANG RECORDS (Records 0 to 1200) ===")
for i in range(0, 1200):
    if doc.records[i]['tag'] in (2201, 2202):
        txt = doc.records[i]['payload'].decode('utf-16le', errors='ignore')
        if any(w in txt for w in ['MASRIYAH', 'SAMIAN', 'Cabang', 'Branch', 'KCP', 'Aries', 'Nama', 'Name']):
            print(f"Record [{i}] Tag {doc.records[i]['tag']}: {txt!r}")
            # Find preceding Tag 2100
            for j in range(i, max(0, i-25), -1):
                if doc.records[j]['tag'] == 2100:
                    coords = struct.unpack(f'<{len(doc.records[j]["payload"])//4}i', doc.records[j]["payload"])
                    print(f"   Preceding Tag 2100 at [{j}]: {coords} (X={coords[0]/28346.4567:.3f}cm, Y={coords[1]/28346.4567:.3f}cm)")
                    break
