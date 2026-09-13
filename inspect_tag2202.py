from xar_dom_engine import XarDocument

t7_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7.xar'
d7 = XarDocument(t7_file)

count = 0
for i, r in enumerate(d7.records):
    if r['tag'] == 2202:
        count += 1
        print(f"Tag 2202 #{count} at Record {i}: len={len(r['payload'])}, payload={repr(r['payload'])}")
        if i > 1500:
            break
