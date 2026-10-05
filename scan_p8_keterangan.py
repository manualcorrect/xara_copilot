import struct
from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

print('=== SCAN KETERANGAN DI PAGE 8 0.XAR VS 0_OUTPUT.XAR ===')

for idx, r in enumerate(doc_0.records):
    if idx > 20000 and r['tag'] == 2150 and len(r['payload']) >= 4:
        w_0 = struct.unpack('<i', r['payload'][:4])[0]
        # Cari di doc_out pada record yang sesuai
        # Cari teks uraian
        txt = ''
        for k in range(idx, min(len(doc_0.records), idx+20)):
            if doc_0.records[k]['tag'] in (2201, 2202):
                t = doc_0.records[k]['payload'].decode('utf-16le', errors='ignore')
                if len(t) > 5 and 'Menara' not in t and 'e-Stat' not in t:
                    txt = t
                    break
        if txt and ('Pembayaran' in txt or 'Danatopup' in txt or 'Transfer' in txt or 'Penarikan' in txt):
            print(f'Rec {idx:5d}: W={w_0:6d} mp ({w_0/72000*2.54:.3f} cm) -> Text: {repr(txt[:50])}')
