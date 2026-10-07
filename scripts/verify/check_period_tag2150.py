from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')

print('Searching backwards from 1050...')
for k in range(1050, 950, -1):
    r = doc.records[k]
    tag = r['tag']
    txt = r['payload'].decode('utf-16le', errors='ignore') if tag in (2201, 2202) else ''
    print(f'Rec {k} Tag {tag}: {txt if txt else r["payload"].hex()[:16]}')
