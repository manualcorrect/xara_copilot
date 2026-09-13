from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

print("=" * 80)
print("COMPARING ROW 10 (2.181.835,81) vs ROW 1 (395.950,81) vs ROW 56 (146.335,81)")
print("=" * 80)

def dump_range(label, start, end):
    print(f"\n--- {label} (Recs {start} to {end}) ---")
    for i in range(start, end + 1):
        rec = doc0.records[i]
        tag = rec['tag']
        text = rec['payload'].decode('utf-16le', errors='ignore') if tag in (2201, 2202) else ''
        hex_data = rec['payload'].hex()
        extra = ""
        if tag == 2100 and len(rec['payload']) >= 12:
            mat = struct.unpack('<iii', rec['payload'][:12])
            x_cm = mat[0] * 2.54 / 72000
            y_cm = mat[1] * 2.54 / 72000
            extra = f"X={x_cm:.4f}cm (mp={mat[0]}), Y={y_cm:.4f}cm"
        elif tag == 2206 and len(rec['payload']) >= 12:
            adv = struct.unpack('<iii', rec['payload'][:12])
            extra = f"adv={adv}"
        elif tag == 2204 and len(rec['payload']) >= 8:
            kern = struct.unpack('<ii', rec['payload'][:8])
            x_cm = kern[0] * 2.54 / 72000
            y_cm = kern[1] * 2.54 / 72000
            extra = f"kern=(dx={kern[0]} [={x_cm:.4f}cm], dy={kern[1]} [={y_cm:.4f}cm])"
        print(f"  Rec {i:5d}: Tag {tag:4d} | text='{text}' | {extra}")

dump_range("Row 1 Saldo", 1570, 1590)
dump_range("Row 10 Saldo", 2885, 2905)
dump_range("Row 56 Saldo (0.xar)", 13575, 13595)
dump_range("Row 56 Nominal (0.xar)", 13600, 13630)
