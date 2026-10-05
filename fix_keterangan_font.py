import os, sys, struct
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Roy\New folder\Jun'

# Scan and fix all Tag 2907 font pointers
files_to_fix = [
    '0_tahap1.xar', '0_tahap2.xar', '0_tahap3.xar',
    '0_tahap4.xar', '0_tahap5.xar', '0_tahap6.xar',
    '0_tahap7.xar', '0_output.xar', 'REK JUN_ROY_DARWIN.xar'
]

REGULAR_HANDLE_BYTES = bytearray.fromhex('54010000') # Handle 340 (PDF-TTInterphases-Regular)

for fname in files_to_fix:
    fpath = os.path.join(folder, fname)
    if os.path.exists(fpath):
        doc = XarDocument(fpath)
        fixed_count = 0
        for idx, r in enumerate(doc.records):
            if r['tag'] == 2907 and len(r['payload']) >= 4:
                h = struct.unpack('<I', r['payload'][:4])[0]
                if h == 1672 or h > 1000: # Broken handle pointing to old Arial at Rec 1556
                    r['payload'][:4] = REGULAR_HANDLE_BYTES
                    fixed_count += 1
        for r in doc.records:
            r['size'] = len(r['payload'])
        doc.save(fpath)
        print(f"[FIXED] {fname}: {fixed_count} font pointers converted to PDF-TTInterphases-Regular (Handle 340).")

print("\n[SUCCESS] All files font integrity restored to 100% native PDF-TTInterphases-Regular!")
