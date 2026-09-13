from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

print("=" * 80)
print("INSPECTING ALL 73 ROWS: ROW NO, TAG 2204 KERN, AND SALDO IN 0.xar")
print("=" * 80)

# Search for row number and following saldo
for i in range(len(doc0.records)):
    r = doc0.records[i]
    if r['tag'] == 2204 and i + 6 < len(doc0.records):
        # check if next text node is saldo
        for k in range(i+1, min(len(doc0.records), i+10)):
            rk = doc0.records[k]
            if rk['tag'] in (2201, 2202):
                txt = rk['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if ',' in txt and (txt.endswith(',81') or txt.endswith(',00')):
                    # check previous text node (row number)
                    prev_txt = ""
                    for p in range(max(0, i-10), i):
                        rp = doc0.records[p]
                        if rp['tag'] in (2201, 2202):
                            prev_txt = rp['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                    
                    dx, dy = struct.unpack('<ii', r['payload'][:8])
                    print(f"Row {prev_txt:3s} | Tag 2204 Rec {i:5d}: dx={dx:6d} ({dx*2.54/72000:.4f}cm), dy={dy} | Saldo Rec {k:5d}: '{txt}'")
                    break
