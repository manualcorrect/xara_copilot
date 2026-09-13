from xar_dom_engine import XarDocument
import re

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# Let's search each page for all text records that represent numbers with ',' or '.'
pages = [
    ("Page 1 (Rows 1-10)", 1190, 3800),
    ("Page 2 (Rows 11-22)", 3920, 6800),
    ("Page 3 (Rows 23-34)", 6930, 9700),
    ("Page 4 (Rows 35-46)", 9870, 12600),
    ("Page 5 (Row 47)", 12750, 14392)
]

for pname, pstart, pend in pages:
    print(f"\n=================== {pname} ===================")
    found_numbers = []
    for i in range(pstart, pend):
        r = doc.records[i]
        if r['tag'] in (2201, 2202):
            s = r['payload'].decode('utf-16le', errors='replace')
            # Check if looks like transaction number or part of number
            if any(c in s for c in [',00', ',0', '+', '-']) or re.search(r'\d+\.\d+', s) or (s.strip() in ['00', '0', '0,00', '0,0']):
                # Find preceding Tag 150, Tag 2100, Tag 2206
                color_tag = None
                matrix_x = None
                width_mp = None
                for j in range(max(0, i-15), i):
                    rj = doc.records[j]
                    if rj['tag'] == 150:
                        color_tag = (j, rj['payload'].hex())
                    elif rj['tag'] == 2100 and len(rj['payload']) == 12:
                        # struct matrix
                        import struct
                        # x is at offset 4 or 8
                        # Let's inspect raw
                        matrix_x = (j, rj['payload'].hex())
                    elif rj['tag'] == 2206 and len(rj['payload']) == 12:
                        import struct
                        w = struct.unpack('<iii', rj['payload'])
                        width_mp = (j, w[0])
                found_numbers.append((i, r['tag'], s, color_tag, width_mp))
    print(f"Total number-like text records: {len(found_numbers)}")
    for fn in found_numbers:
        print(f"  Rec {fn[0]:5d} [Tag {fn[1]}]: text={repr(fn[2]):18s} | Color={fn[3]} | Width={fn[4]}")
