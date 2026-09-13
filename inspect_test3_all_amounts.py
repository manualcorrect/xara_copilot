from xar_dom_engine import XarDocument
import struct

MP_PER_CM = 72000 / 2.54

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')

# Let's collect all nominal and saldo rows in test_3.1.xar
# We know their Y ranges
# Page 1 (rows 1-10): Y from 492000 down to 78000
# Page 2 (rows 11-14): Y from 608000 down to 470000
# Page 3 (rows 15-17): Y from 424000 down to 332000

print(f"{'Text':18s} | {'Tag2100 MX':10s} | {'Tag2206 W':10s} | {'Right Edge (mp)':15s} | {'Right Edge (cm)':15s}")
print("-" * 75)

for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
        if any(c.isdigit() for c in txt) and (',' in txt or '.' in txt):
            mx, my, w = None, None, None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 2100:
                    mx, my = struct.unpack('<ii', doc.records[k]['payload'][:8])
                    break
            for k in range(max(0, i-15), i):
                if doc.records[k]['tag'] == 2206:
                    w = struct.unpack('<i', doc.records[k]['payload'][:4])[0]
                    break
            if mx and mx > 300000 and my and my < 700000:
                tot = mx + w
                print(f"{txt:18s} | {mx:10d} | {w:10d} | {tot:15d} | {tot/MP_PER_CM:12.3f} cm")
