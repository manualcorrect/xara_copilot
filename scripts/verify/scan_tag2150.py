import struct
from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

print('=== SCAN ALL TAG 2150 IN 0.XAR ===')
for idx, r in enumerate(doc_0.records):
    if r['tag'] == 2150 and len(r['payload']) >= 4:
        w = struct.unpack('<i', r['payload'][:4])[0]
        # Cari teks terdekat setelahnya
        txt = ''
        for k in range(idx, min(len(doc_0.records), idx+15)):
            if doc_0.records[k]['tag'] in (2201, 2202):
                txt = doc_0.records[k]['payload'].decode('utf-16le', errors='ignore')
                break
        if 50000 <= w <= 200000:
            print(f'Rec {idx:5d}: W={w:6d} mp ({w/72000*2.54:.3f} cm) -> Text: {repr(txt[:40])}')
