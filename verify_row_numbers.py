from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Let's inspect text nodes between row starts
expected_row_nums = [
    (1, [1518, 1523]),
    (2, [1758]),
    (3, [1888, 1893]),
    (4, [2059, 2064]),
    (5, [2296]),
    (6, [2416, 2421]),
    (7, [2582, 2587]),
    (8, [2803]),
    (9, [2994]),
    (10, [3124, 3129]),
    (11, [4195]),
    (12, [4381]),
    (13, [4567]),
    (14, [4692, 4697]),
    (15, [4858, 4863]),
    (16, [5094]),
    (17, [5280]),
    (18, [5410, 5415]),
    (19, [5576, 5581]),
    (20, [5768, 5773]),
    (21, [5949, 5969]),
    (22, [6104, 6130])
]

for row_idx, recs in expected_row_nums:
    txts = []
    for r in recs:
        try:
            txts.append(doc.records[r]['payload'].decode('utf-16le').rstrip('\x00'))
        except:
            txts.append("ERR")
    print(f"Row {row_idx:2d}: recs {recs} -> {''.join(txts)}")
