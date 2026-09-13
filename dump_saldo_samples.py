from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

data = []
for i in range(len(doc0.records)):
    r = doc0.records[i]
    if r['tag'] == 2204 and i + 6 < len(doc0.records):
        for k in range(i+1, min(len(doc0.records), i+10)):
            rk = doc0.records[k]
            if rk['tag'] in (2201, 2202):
                txt = rk['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if ',' in txt and (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0'):
                    # Also find row number
                    row_txt = ""
                    for p in range(max(0, i-10), i):
                        if doc0.records[p]['tag'] in (2201, 2202):
                            row_txt = doc0.records[p]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                    dx, dy = struct.unpack('<ii', r['payload'][:8])
                    data.append((row_txt, txt, dx, dy, i, k))
                    break

print(f"Total samples: {len(data)}")
for r_no, s_txt, dx, dy, i_rec, k_rec in data:
    print(f"Row {r_no:3s} | Saldo: '{s_txt:14s}' | Tag 2204 Rec {i_rec:5d}: dx={dx:6d}, dy={dy:8d}")
