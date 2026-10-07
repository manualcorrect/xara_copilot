import struct
from xar_dom_engine import XarDocument

def collect_samples(path):
    doc = XarDocument(path)
    samples = []
    for i, r in enumerate(doc.records):
        if r['tag'] == 2206:
            w = struct.unpack('<i', r['payload'][:4])[0]
            # find text
            for k in range(i+1, min(len(doc.records), i+5)):
                if doc.records[k]['tag'] in [2201, 2202]:
                    txt = doc.records[k]['payload'].decode('utf-16le', errors='replace').strip('\x00')
                    # We only care about numbers/amounts in the table
                    if any(c.isdigit() for c in txt) and (',' in txt or '.' in txt or txt.startswith('+') or txt.startswith('-')):
                        # Check if font size is the table font (H=6559 in Tag 2206)
                        h = struct.unpack('<i', r['payload'][4:8])[0] if len(r['payload']) >= 8 else 0
                        if h == 6559:
                            samples.append((txt, w))
                    break
    return samples

s1 = collect_samples(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
s2 = collect_samples(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap6.xar')

all_samples = list(set(s1 + s2))
print(f"Total unique amount samples with H=6559: {len(all_samples)}")
for txt, w in sorted(all_samples, key=lambda x: len(x[0])):
    print(f"  {txt:18s} : {w:6d} mp ({w/28346.4567:.3f} cm)")
