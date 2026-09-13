from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')

# Let's inspect stories around Y=492000 (Row 1) in test_3.1.xar
for i, r in enumerate(doc.records):
    if r['tag'] == 2100:
        p = r['payload']
        ints = struct.unpack(f"<{len(p)//4}i", p[:(len(p)//4)*4])
        if len(ints) >= 2 and ints[1] == 492000:
            # find text
            txt = ""
            w = 0
            for k in range(i+1, min(len(doc.records), i+25)):
                if doc.records[k]['tag'] == 2206:
                    w = struct.unpack('<i', doc.records[k]['payload'][:4])[0]
                elif doc.records[k]['tag'] == 2201:
                    txt = doc.records[k]['payload'].decode('utf-16le', errors='replace').strip('\x00')
                    break
            print(f"[{i}] Row 1 item: '{txt}' | MX={ints[0]} | W={w} | Right={ints[0] + w} ({(ints[0]+w)/28346.4567:.3f} cm)")
