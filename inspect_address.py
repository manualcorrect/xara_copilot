import struct
from xar_dom_engine import XarDocument

jun = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap7.xar')
print('=== JUN SURROUNDINGS (rec 290..315) ===')
for i in range(290, 315):
    r = jun.records[i]
    tag = r['tag']
    txt = ''
    if tag in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
    elif tag == 2100:
        txt = f'Coords: {struct.unpack("<iii", r["payload"][:12])}'
    elif tag == 2206:
        txt = f'Kern: {struct.unpack("<iii", r["payload"][:12])}'
    elif tag == 2200:
        txt = 'TAG_TEXT_STORY'
    print(f'{i}: Tag {tag} {txt}')

print('\n=== JUN SURROUNDINGS (rec 3365..3388) ===')
for i in range(3365, 3388):
    r = jun.records[i]
    tag = r['tag']
    txt = ''
    if tag in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
    elif tag == 2100:
        txt = f'Coords: {struct.unpack("<iii", r["payload"][:12])}'
    elif tag == 2206:
        txt = f'Kern: {struct.unpack("<iii", r["payload"][:12])}'
    elif tag == 2200:
        txt = 'TAG_TEXT_STORY'
    print(f'{i}: Tag {tag} {txt}')

agu = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar')
print('\n=== AGU SURROUNDINGS (rec 5280..5320) ===')
for i in range(5280, 5320):
    r = agu.records[i]
    tag = r['tag']
    txt = ''
    if tag in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
    elif tag == 2100:
        txt = f'Coords: {struct.unpack("<iii", r["payload"][:12])}'
    elif tag == 2206:
        txt = f'Kern: {struct.unpack("<iii", r["payload"][:12])}'
    elif tag == 2200:
        txt = 'TAG_TEXT_STORY'
    print(f'{i}: Tag {tag} {txt}')
