from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

print('=== 0.XAR ALL DANATOPUP ===')
for i, r in enumerate(doc_0.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Danatopup' in txt or 'Dan' in txt:
            print(f'0.xar Rec {i}: {repr(txt)}')

print('=== 0_OUTPUT.XAR ALL DANATOPUP ===')
for i, r in enumerate(doc_out.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Danatopup' in txt or 'Dan' in txt:
            print(f'0_out Rec {i}: {repr(txt)}')
