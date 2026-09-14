import os
import struct
from xar_dom_engine import XarDocument

p = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(p)

print("=== ALL HEADERS CONTEXT SCAN IN AUG/0.XAR ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if any(w in txt for w in ['Periode', 'Period', 'Dicetak', 'Printed', 'No. Rekening', 'Account No', 'Halaman', 'Page', 'Closing Balance', 'Saldo Awal', 'Opening Balance']):
            print(f"\n--- MATCH AT REC {i}: {txt!r} ---")
            for j in range(max(0, i-5), min(len(doc.records), i+25)):
                rj = doc.records[j]
                tag = rj['tag']
                pl = rj['payload']
                extra = ""
                if tag in (2201, 2202):
                    extra = f"TEXT: {pl.decode('utf-16le', errors='ignore')!r}"
                elif tag == 2100:
                    coords = struct.unpack(f'<{len(pl)//4}i', pl)
                    extra = f"COORDS: {coords}"
                elif tag == 2150:
                    w, fl = struct.unpack('<iB', pl)
                    extra = f"BOX: w={w}, flag={fl}"
                elif tag == 2206:
                    t6 = struct.unpack('<iii', pl[:12])
                    extra = f"T2206: {t6}"
                elif tag in (150, 2901, 2906, 2907, 4208, 4209):
                    extra = f"HEX: {pl.hex()}"
                print(f"  [{j:5d}] Tag {tag:4d}: {extra}")
