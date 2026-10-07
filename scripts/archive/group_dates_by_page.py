from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(target_file)

# Let's group transactions by page and order
pages = [
    ("Page 1", 1190, 3800),
    ("Page 2", 3920, 6800),
    ("Page 3", 6930, 9700),
    ("Page 4", 9870, 12600),
    ("Page 5", 12750, 14392)
]

# In each page, let's find all date occurrences and check the year 2025 -> 2026
for pname, start, end in pages:
    print(f"\n=================== {pname} ===================")
    for i in range(start, end):
        r = doc.records[i]
        if r['tag'] in (2201, 2202):
            s = r['payload'].decode('utf-16le', errors='replace')
            if 'Apr' in s or '2025' in s or '202' in s:
                # print record info
                print(f"Record {i:5d} | Tag {r['tag']} | len={len(r['payload']):2d} | text={repr(s)}")
