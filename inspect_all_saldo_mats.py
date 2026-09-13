from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

print("=" * 80)
print("INSPECTING SALDO & NOMINAL MATRICES ACROSS ALL 73 ROWS")
print("=" * 80)

# Let's find all text objects for saldo on each page
# In 0.xar, saldo strings end with ',81' or similar
for i, rec in enumerate(doc0.records):
    if rec['tag'] in (2201, 2202):
        txt = rec['payload'].decode('utf-16le', errors='ignore')
        if txt.endswith(',81') and len(txt) >= 6:
            # check parent tag 2100
            for k in range(max(0, i-25), i):
                if doc0.records[k]['tag'] == 2100:
                    mat = struct.unpack('<iii', doc0.records[k]['payload'][:12])
                    x_cm = mat[0] * 2.54 / 72000
                    y_cm = mat[1] * 2.54 / 72000
                    print(f"Rec {i:5d}: Saldo='{txt:14s}' | Tag 2100 Rec {k:5d}: X={x_cm:.4f}cm (mp={mat[0]}), Y={y_cm:.4f}cm")
                    break
