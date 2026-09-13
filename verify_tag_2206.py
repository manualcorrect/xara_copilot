import struct
from xar_dom_engine import XarDocument

def check_doc(path):
    print(f"\nChecking: {path}")
    doc = XarDocument(path)
    for i, r in enumerate(doc.records):
        if r['tag'] == 2206:
            p = r['payload']
            ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
            # check if following record is 2201 (string)
            txt = ""
            for k in range(i+1, min(len(doc.records), i+5)):
                if doc.records[k]['tag'] == 2201:
                    txt = doc.records[k]['payload'].decode('utf-16le', errors='replace').strip('\x00')
                    break
                elif doc.records[k]['tag'] == 2202:
                    txt = doc.records[k]['payload'].decode('utf-16le', errors='replace').strip('\x00')
                    break
            if txt and any(c.isdigit() for c in txt) and (',' in txt or '.' in txt):
                print(f"[{i:5d}] Tag 2206: W={ints[0]:6d}, H={ints[1]:5d} | Text: '{txt}'")

check_doc(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
