import numpy as np
from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

# Collect all (row_str, saldo_str, dx, dy)
data = []
for i in range(len(doc0.records)):
    r = doc0.records[i]
    if r['tag'] == 2204 and i + 6 < len(doc0.records):
        for k in range(i+1, min(len(doc0.records), i+10)):
            rk = doc0.records[k]
            if rk['tag'] in (2201, 2202):
                txt = rk['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if ',' in txt and (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0'):
                    dx, dy = struct.unpack('<ii', r['payload'][:8])
                    data.append((txt, dx, dy))
                    break

print(f"Total valid samples: {len(data)}")
for txt, dx, dy in data[:10]:
    print(f"'{txt:14s}' -> dx={dx}, dy={dy}")
