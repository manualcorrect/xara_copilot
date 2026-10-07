from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(target_file)

months = ['Apr', 'Dec', 'Jan', 'Feb', 'Mar', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov']

for p_idx, p_range in enumerate([
    (1190, 3800),
    (3920, 6800),
    (6930, 9700),
    (9870, 12600),
    (12750, 14392)
]):
    print(f"=== PAGE {p_idx+1} ===")
    for i in range(p_range[0], p_range[1]):
        r = doc.records[i]
        if r['tag'] in (2201, 2202):
            s = r['payload'].decode('utf-16le', errors='replace')
            if any(m in s for m in months) or ':' in s:
                print(f"  Rec {i} [Tag {r['tag']}]: {repr(s)}")
