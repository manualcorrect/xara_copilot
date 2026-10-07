import struct
from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

pages = [i for i, r in enumerate(doc_0.records) if r['tag'] == 46]
print('Page spread indices in 0.xar:', pages)

p8_start = pages[7]
p8_end = pages[8] if len(pages) > 8 else len(doc_0.records)
print(f'Page 8 range: Rec {p8_start} to {p8_end}')

print('\n=== TEXTS ON PAGE 8 OF 0.XAR ===')
for i in range(p8_start, min(p8_end, p8_start + 400)):
    r = doc_0.records[i]
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        print(f'  Rec {i} Tag {r["tag"]}: {repr(txt)}')
