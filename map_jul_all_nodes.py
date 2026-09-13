import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Y coordinates for the 22 rows:
# Page 1:
# Row 1: Y=492117
# Row 2: Y=446117
# Row 3: Y=400117
# Row 4: Y=354117
# Row 5: Y=308117
# Row 6: Y=262117
# Row 7: Y=216117
# Row 8: Y=170117
# Row 9: Y=124117
# Row 10: Y=78117
# Page 2:
# Row 11: Y=608000
# Row 12: Y=562000
# Row 13: Y=516000
# Row 14: Y=470000
# Row 15: Y=424000
# Row 16: Y=378000
# Row 17: Y=332000
# Row 18: Y=286000
# Row 19: Y=240000
# Row 20: Y=194000
# Row 21: Y=148000
# Row 22: Y=102000

# Let's inspect the records around each row by defining range of records between row start and row end.
# In Story 935:
# Let's trace all records in Story 935 (from rec 935 to rec 6300)
story_records = []
for i in range(935, 6300):
    r = doc.records[i]
    tag = r['tag']
    txt = ""
    if tag in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
        except:
            pass
    tag_info = ""
    if tag == 2100:
        vals = struct.unpack('<iii', r['payload'][:12])
        tag_info = f"2100: x={vals[0]}, y={vals[1]}, p={vals[2]}"
    elif tag == 2206:
        vals = struct.unpack('<iii', r['payload'][:12])
        tag_info = f"2206: w={vals[0]}, h={vals[1]}"
    elif tag == 150:
        tag_info = f"150: col={r['payload'].hex()}"
    
    story_records.append((i, tag, txt, tag_info))

print("Total records traced:", len(story_records))

# Let's find each of the 22 nominal records and examine everything around it!
nom_candidates = [
    (1, 1587), (2, 1778), (3, 1949), (4, 2115), (5, 2316),
    (6, 2477), (7, 2643), (8, 2823), (9, 3014), (10, 3192),
    (11, 4215), (12, 4401), (13, 4587), (14, 4753), (15, 4929),
    (16, 5114), (17, 5300), (18, 5471), (19, 5632), (20, 5808),
    (21, 5994), (22, 6160)
]

for row_idx, nom_idx in nom_candidates:
    print(f"\n==================== ROW {row_idx} (Nominal around {nom_idx}) ====================")
    # print all records from nom_idx - 70 to nom_idx + 45
    start_j = max(935, nom_idx - 70)
    end_j = min(6300, nom_idx + 45)
    for j in range(start_j, end_j):
        r = doc.records[j]
        tag = r['tag']
        if tag in (2201, 2202):
            try:
                t = r['payload'].decode('utf-16le').rstrip('\x00')
                print(f"  Rec {j:4d} | Tag {tag:4d} | TXT: {repr(t)}")
            except:
                pass
        elif tag == 2100:
            vals = struct.unpack('<iii', r['payload'][:12])
            print(f"  Rec {j:4d} | Tag 2100 | (x={vals[0]}, y={vals[1]})")
        elif tag == 2206:
            vals = struct.unpack('<iii', r['payload'][:12])
            print(f"  Rec {j:4d} | Tag 2206 | (w={vals[0]}, h={vals[1]})")
        elif tag == 150:
            print(f"  Rec {j:4d} | Tag  150 | col={r['payload'].hex()}")
