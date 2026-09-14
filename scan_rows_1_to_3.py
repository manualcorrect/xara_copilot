from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar')

print("=== ROW 1 TO ROW 3 DETAILED SCAN IN 0.XAR ===")
for i in range(1550, 2050):
    r = doc.records[i]
    if r['tag'] in (2201, 2202, 2204, 2100):
        pl = r['payload']
        if r['tag'] in (2201, 2202):
            print(f"[{i:5d}] Tag {r['tag']:4d}: TEXT = {pl.decode('utf-16le', errors='ignore')!r}")
        elif r['tag'] == 2204:
            print(f"[{i:5d}] Tag 2204")
        elif r['tag'] == 2100:
            print(f"[{i:5d}] Tag 2100")
