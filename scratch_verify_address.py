import struct
from xar_dom_engine import XarDocument

jun_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap7.xar'
agu_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0_output.xar'

jun = XarDocument(jun_path)
agu = XarDocument(agu_path)

print('Jun records count:', len(jun.records))
print('Agu records count:', len(agu.records))

def dump_story(doc, start, end, label):
    print(f'=== {label} ({start}..{end}) ===')
    full_str = ''
    for i in range(start, end+1):
        r = doc.records[i]
        tag = r['tag']
        p = r['payload']
        if tag == 2206:
            w, h, dx = struct.unpack('<iii', p[:12])
            print(f'  Rec {i} [Tag {tag}]: advance=({w}, {h}, {dx})')
        elif tag in (2201, 2202):
            try:
                s = p.decode('utf-16le', errors='replace')
                if s != '\x00':
                    full_str += s
                print(f'  Rec {i} [Tag {tag}]: {repr(s)} (bytes={len(p)})')
            except Exception as e:
                print(f'  Rec {i} [Tag {tag}]: raw={p.hex()}')
        elif tag == 2204:
            dx, dy = struct.unpack('<ii', p[:8])
            if dx != 0 or dy != 0:
                print(f'  Rec {i} [Tag {tag}]: kern=({dx}, {dy})')
        elif tag == 2100:
            x, y, flag = struct.unpack('<iii', p[:12])
            print(f'  Rec {i} [Tag {tag}]: matrix origin=({x}, {y}, {flag})')
    print(f'  Full string: {repr(full_str)}')

dump_story(jun, 302, 314, 'JUN PAGE 1')
dump_story(agu, 305, 435, 'AGU PAGE 1')
dump_story(agu, 5295, 5312, 'AGU PAGE 2')
dump_story(agu, 8493, 8623, 'AGU PAGE 3')
