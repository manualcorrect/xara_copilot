import json
import struct
from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

print(f"Total Records: {len(doc.records)}")

def get_text(idx):
    if 0 <= idx < len(doc.records):
        r = doc.records[idx]
        if r['tag'] in (2201, 2202, 2203):
            return r['payload'].decode('utf-16le', errors='ignore')
    return ""

def get_tag(idx):
    if 0 <= idx < len(doc.records):
        return doc.records[idx]['tag']
    return None

# Let's find each row 1 to 19
# Row 1 is on page 1, let's map all 19 rows
rows = []

# Let's inspect records around rows
# Let's write a scanner that identifies transaction row blocks
for i, r in enumerate(doc.records):
    txt = get_text(i)
    # Check if this is a row number or date or amount
    if txt in [str(n) for n in range(1, 20)]:
        print(f"Candidate Row No {txt}: Rec {i} (Tag {r['tag']})")

