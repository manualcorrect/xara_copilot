from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap5.xar'
doc = XarDocument(target_file)

split_records = [
    4382, 4529, 4676, 4835, 4999, 5162, 5324, 5503, 5676,
    7880, 8386, 8556, 8724, 8861, 8973, 9110,
    10260, 10417, 10579, 10757, 10904, 11056, 11203, 11360, 11497
]

for idx in split_records:
    r = doc.records[idx]
    s = r['payload'].decode('utf-16le', errors='replace')
    # Find next text record
    found_next = None
    for j in range(idx+1, idx+15):
        rj = doc.records[j]
        if rj['tag'] in (2201, 2202):
            sj = rj['payload'].decode('utf-16le', errors='replace')
            found_next = (j, rj['tag'], sj)
            break
    print(f"Record {idx} ({repr(s)}) -> Next: {found_next}")
