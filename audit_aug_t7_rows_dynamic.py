import os
import struct
import json
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug'
t7_path = os.path.join(folder, '0_tahap7.xar')

doc = XarDocument(t7_path)

print("=== AUDITING ALL 110 ROWS IN 0_TAHAP7.XAR DYNAMICALLY ===")
# Find all rows in doc by scanning Tag 2204 or Saldo values
rows_found = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2204 and i > 1200:
        # check next few records for saldo
        for k in range(i+1, min(len(doc.records), i+8)):
            if doc.records[k]['tag'] in (2201, 2202):
                txt = doc.records[k]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0') and ('.' in txt or len(txt) > 5):
                    # Check if preceding has row number or context
                    rows_found.append((i, k, txt))
                    break

print(f"Total Saldo rows detected in 0_tahap7.xar: {len(rows_found)}")
for idx, rf in enumerate(rows_found[:15], 1):
    print(f"Row {idx:3d}: Tag2204 at {rf[0]:5d} | Saldo at {rf[1]:5d}: {rf[2]!r}")
print("...")
for idx, rf in enumerate(rows_found[-5:], len(rows_found)-4):
    print(f"Row {idx:3d}: Tag2204 at {rf[0]:5d} | Saldo at {rf[1]:5d}: {rf[2]!r}")
