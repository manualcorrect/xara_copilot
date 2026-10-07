import struct
from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

def inspect_keterangan_fuzzy(doc, label):
    print(f'=== {label} ===')
    matches = []
    for i, r in enumerate(doc.records):
        if r['tag'] in (2201, 2202):
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if 'Danatopup' in txt or '89508089622130569' in txt:
                matches.append((i, txt))
    print(f'Matches count: {len(matches)}')
    for idx, (rec_i, txt) in enumerate(matches):
        print(f'{idx+1}. Rec {rec_i}: {repr(txt)}')
        # Cari tag 2100 dan 2150 terdekat sebelumnya
        for k in range(rec_i-1, max(0, rec_i-30), -1):
            if doc.records[k]['tag'] == 2150:
                w = struct.unpack('<i', doc.records[k]['payload'][:4])[0]
                print(f'     Tag 2150 Rec {k}: W={w} mp ({w/72000*2.54:.3f} cm)')
            elif doc.records[k]['tag'] == 2100:
                coords = struct.unpack('<iii', doc.records[k]['payload'][:12])
                print(f'     Tag 2100 Rec {k}: X={coords[0]} ({coords[0]/72000*2.54:.3f} cm), Y={coords[1]} ({coords[1]/72000*2.54:.3f} cm)')
                break

inspect_keterangan_fuzzy(doc_0, '0.xar (Original)')
inspect_keterangan_fuzzy(doc_out, '0_output.xar (Output)')
