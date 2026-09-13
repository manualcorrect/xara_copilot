from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap1.xar'
doc = XarDocument(target_file)

for page, start, end in [
    (1, 1070, 1095),
    (2, 3870, 3895),
    (3, 6875, 6900),
    (4, 9820, 9845),
    (5, 12705, 12730)
]:
    print(f"\n=== Page {page} Period Block ({start}..{end}) ===")
    for k in range(start, end):
        r = doc.records[k]
        if r['tag'] in (2200, 2201, 2202, 2203, 2206, 0, 1):
            val = r['payload'].decode('utf-16le', errors='replace') if r['tag'] in (2201, 2202) else (r['payload'].hex() if r['tag'] == 2206 else '')
            print(f"Rec {k:05d} Tag {r['tag']:04d} len={len(r['payload']):03d}: {repr(val)}")
