from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar')

print("=" * 80)
print("INSPECTING SALDO & NOMINAL NODES AROUND ROWS 50-58")
print("=" * 80)

# Rows and their saldo records:
# Row 50: 12689
# Row 51: 12844
# Row 52: 12994
# Row 53: 13134
# Row 54: 13287
# Row 55: 13437
# Row 56: 13587
# Row 57: 13739
# Row 58: 13889

for r_name, r_idx in [
    ("Row 50 Saldo", 12689),
    ("Row 51 Saldo", 12844),
    ("Row 52 Saldo", 12994),
    ("Row 53 Saldo", 13134),
    ("Row 54 Saldo", 13287),
    ("Row 55 Saldo", 13437),
    ("Row 56 Saldo", 13587),
    ("Row 57 Saldo", 13739),
    ("Row 58 Saldo", 13889),
]:
    print(f"\n--- {r_name} (Rec {r_idx}) ---")
    # print preceding 10 records
    for i in range(r_idx - 10, r_idx + 15):
        rec = doc7.records[i]
        tag = rec['tag']
        text = rec['payload'].decode('utf-16le', errors='ignore') if tag in (2201, 2202) else ''
        hex_data = rec['payload'].hex()
        adv = struct.unpack('<iii', rec['payload'][:12]) if tag == 2206 and len(rec['payload']) >= 12 else ''
        print(f"  Rec {i:5d}: Tag {tag:4d} | size={rec['size']:3d} | text='{text}' | hex={hex_data[:20]} | adv={adv}")
