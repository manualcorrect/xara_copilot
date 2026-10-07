import os
import struct
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'

for fname in ['0.xar', '0_tahap1.xar', '0_tahap6.xar', '0_tahap7.xar']:
    fpath = os.path.join(folder, fname)
    if os.path.exists(fpath):
        doc = XarDocument(fpath)
        print(f"File {fname:15s}: {len(doc.records):,} records")
