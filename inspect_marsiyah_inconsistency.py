from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')
doc6 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap6.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar')

print("=" * 80)
print("INSPECTING MARSIYAH ROWS 50 - 58")
print("=" * 80)

# Let's inspect records from 12500 to 14200
for i in range(12500, 14200):
    r0 = doc0.records[i]
    r6 = doc6.records[i]
    r7 = doc7.records[i]
    
    t0 = r0['payload'].decode('utf-16le', errors='ignore') if r0['tag'] in (2201, 2202) else ''
    t6 = r6['payload'].decode('utf-16le', errors='ignore') if r6['tag'] in (2201, 2202) else ''
    t7 = r7['payload'].decode('utf-16le', errors='ignore') if r7['tag'] in (2201, 2202) else ''
    
    # Check if there is any interesting tag or change
    if t0 or t6 or t7 or r0['tag'] in (150, 2200, 2206, 2100):
        c0 = r0['payload'].hex() if r0['tag'] == 150 else ''
        c7 = r7['payload'].hex() if r7['tag'] == 150 else ''
        f0 = r0['payload'].hex() if r0['tag'] == 2200 else ''
        f7 = r7['payload'].hex() if r7['tag'] == 2200 else ''
        t2206_0 = struct.unpack('<iii', r0['payload'][:12])[0] if r0['tag'] == 2206 and len(r0['payload']) >= 12 else ''
        t2206_7 = struct.unpack('<iii', r7['payload'][:12])[0] if r7['tag'] == 2206 and len(r7['payload']) >= 12 else ''
        
        # Filter for rows 50-58
        if any(w in t0 for w in ['23 Jun', '24 Jun', '25 Jun', '26 Jun', 'Danatopup', 'PECEL LELE', 'Syarkawi', 'VISIONET', 'RAZIF', '147.335', '186.335', '224.335', '274.335', '275.335', '25.335', '6.502', '6.465', '6.715', '6.355', '-1.000', '-50.000', '-38.000', '-39.000', '+250.000', '-37.000']) or \
           any(w in t7 for w in ['23 Jun', '24 Jun', '25 Jun', '26 Jun', 'Danatopup', 'PECEL LELE', 'Syarkawi', 'VISIONET', 'RAZIF', '147.335', '186.335', '224.335', '274.335', '275.335', '25.335', '6.502', '6.465', '6.715', '6.355', '-1.000', '-50.000', '-38.000', '-39.000', '+250.000', '-37.000']):
            print(f"Rec {i:5d} [Tag {r0['tag']:4d}]: 0.xar=\"{t0}\" | t6=\"{t6}\" | t7=\"{t7}\" | col={c7} font={f7} adv={t2206_7}")
