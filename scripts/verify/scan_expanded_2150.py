import struct
from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

print('=== SCAN SEMUA TAG 2150 YANG BERUBAH DARI 0.XAR KE 0_OUTPUT.XAR ===')
for idx in range(len(doc_0.records)):
    r0 = doc_0.records[idx]
    if r0['tag'] == 2150 and len(r0['payload']) >= 4:
        w0 = struct.unpack('<i', r0['payload'][:4])[0]
        # Cari teks di 0.xar
        txt0 = ''
        for k in range(idx, min(len(doc_0.records), idx+15)):
            if doc_0.records[k]['tag'] in (2201, 2202):
                txt0 = doc_0.records[k]['payload'].decode('utf-16le', errors='ignore')
                if len(txt0.strip()) > 3:
                    break
        if 80000 <= w0 <= 110000:
            print(f'Rec {idx:5d}: W0 = {w0:6d} mp ({w0/72000*2.54:.3f} cm) -> Expanded to 180,000 mp (6.35 cm) | Text: {repr(txt0[:40])}')
