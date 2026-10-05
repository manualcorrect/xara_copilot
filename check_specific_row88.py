import struct
from xar_dom_engine import XarDocument

doc_0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0.xar')
doc_out = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jul\0_output.xar')

print('=== 0.XAR REC 21530 ===')
for k in range(21530-1, 21530-25, -1):
    tag = doc_0.records[k]['tag']
    p = doc_0.records[k]['payload']
    if tag == 2150:
        w = struct.unpack('<i', p[:4])[0]
        print(f'Tag 2150 Rec {k}: W = {w} mp ({w/72000*2.54:.3f} cm)')
    elif tag == 2100:
        print(f'Tag 2100 Rec {k}: {struct.unpack("<iii", p[:12])}')
        break

print('\n=== 0_OUTPUT.XAR REC 22280 ===')
for k in range(22280-1, 22280-25, -1):
    tag = doc_out.records[k]['tag']
    p = doc_out.records[k]['payload']
    if tag == 2150:
        w = struct.unpack('<i', p[:4])[0]
        print(f'Tag 2150 Rec {k}: W = {w} mp ({w/72000*2.54:.3f} cm)')
    elif tag == 2100:
        print(f'Tag 2100 Rec {k}: {struct.unpack("<iii", p[:12])}')
        break
