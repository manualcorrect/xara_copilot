import struct
from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

print('=== DETAIL REC 21514 DI 0.XAR ===')
for i in range(21500, 21535):
    r = doc_0.records[i]
    tag = r['tag']
    p = r['payload']
    txt = p.decode('utf-16le', errors='ignore') if tag in (2201, 2202) else ''
    desc = ''
    if tag == 2150:
        desc = f'W = {struct.unpack("<i", p[:4])[0]} mp'
    elif tag == 2100:
        desc = f'Matrix = {struct.unpack("<iii", p[:12])}'
    print(f'Rec {i} Tag {tag}: {desc} {repr(txt) if txt else ""}')

print('\n=== DETAIL PADA DOC_OUT ===')
for i, r in enumerate(doc_out.records):
    if r['tag'] == 2201 and 'Pembayaran Danatopup 89508089622130569' in r['payload'].decode('utf-16le', errors='ignore') or ('Pembayaran Dan' in r['payload'].decode('utf-16le', errors='ignore') and i > 20000):
        print(f'Found at Rec {i}')
        for k in range(max(0, i-20), min(len(doc_out.records), i+15)):
            rec = doc_out.records[k]
            tag = rec['tag']
            p = rec['payload']
            txt = p.decode('utf-16le', errors='ignore') if tag in (2201, 2202) else ''
            desc = ''
            if tag == 2150:
                desc = f'W = {struct.unpack("<i", p[:4])[0]} mp'
            elif tag == 2100:
                desc = f'Matrix = {struct.unpack("<iii", p[:12])}'
            print(f'  Rec {k} Tag {tag}: {desc} {repr(txt) if txt else ""}')
        break
