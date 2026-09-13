from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar')

print("=" * 100)
print("DETAILED AUDIT OF PAGE 5 (ROWS 50 to 58)")
print("=" * 100)

for i in range(12500, 14000):
    r0 = doc0.records[i]
    r7 = doc7.records[i]
    tag = r0['tag']
    
    # Check text
    if tag in (2201, 2202):
        t0 = r0['payload'].decode('utf-16le', errors='ignore')
        t7 = r7['payload'].decode('utf-16le', errors='ignore')
        print(f"Rec {i:5d} [Tag {tag}]: 0.xar='{t0}' --> 0_tahap7='{t7}'")
    elif tag == 150:
        c0 = r0['payload'].hex()
        c7 = r7['payload'].hex()
        if c0 != c7:
            print(f"Rec {i:5d} [Tag 150 COLOR]: 0.xar={c0} --> 0_tahap7={c7}")
    elif tag == 2206:
        w0 = struct.unpack('<iii', r0['payload'][:12])[0]
        w7 = struct.unpack('<iii', r7['payload'][:12])[0]
        if w0 != w7:
            print(f"Rec {i:5d} [Tag 2206 ADVANCE]: 0.xar={w0} --> 0_tahap7={w7}")
    elif tag == 2200:
        f0 = r0['payload'].hex()
        f7 = r7['payload'].hex()
        if f0 != f7:
            print(f"Rec {i:5d} [Tag 2200 FONT]: 0.xar={f0} --> 0_tahap7={f7}")
