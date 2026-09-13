from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

print("=" * 80)
print("ANALYZING SALDO TAG 2204 DY vs SALDO TEXT IN 0.xar")
print("=" * 80)

# Let's collect all rows where row number and saldo are present
samples = []
for i in range(len(doc0.records)):
    r = doc0.records[i]
    if r['tag'] == 2204 and i + 6 < len(doc0.records):
        for k in range(i+1, min(len(doc0.records), i+10)):
            rk = doc0.records[k]
            if rk['tag'] in (2201, 2202):
                txt = rk['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if ',' in txt and (txt.endswith(',81') or txt.endswith(',00')):
                    dx, dy = struct.unpack('<ii', r['payload'][:8])
                    samples.append((i, k, txt, dx, dy))
                    break

for i, k, txt, dx, dy in samples[:25]:
    print(f"Saldo: '{txt:14s}' | Tag 2204 Rec {i:5d}: dy={dy} | dx={dx}")
