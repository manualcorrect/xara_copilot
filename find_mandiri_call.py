from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar')

print("=== ALL MANDIRI CALL 14000 LOCATIONS ===")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Mandiri Call 14000' in txt:
            # find end of story (Tag 2203)
            for j in range(i, i+10):
                if doc.records[j]['tag'] == 2203:
                    end = j + 1
                    while end < len(doc.records) and doc.records[end]['tag'] == 0:
                        end += 1
                    print(f"Mandiri Call at [{i}], story ends at [{end}]")
                    break
