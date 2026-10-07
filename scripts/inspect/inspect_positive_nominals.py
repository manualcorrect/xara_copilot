from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

print("=" * 80)
print("INSPECTING ROW 51, 58, 10, 18, 27, 31, 41, 45 POSITIVE NOMINALS")
print("=" * 80)

# Positive nominals in 0.xar:
# Row 10 (Rec 2932), Row 18 (Rec 5062), Row 27 (Rec 7352), Row 31 (Rec 7968), Row 41 (Rec 10435), Row 45 (Rec 11025), Row 51 (Rec 12877), Row 58 (Rec 13922)
for r_name, rec_idx in [
    ("Row 10", 2932),
    ("Row 18", 5062),
    ("Row 27", 7352),
    ("Row 31", 7968),
    ("Row 41", 10435),
    ("Row 45", 11025),
    ("Row 51", 12877),
    ("Row 58", 13922),
]:
    print(f"\n--- {r_name} (around rec {rec_idx}) ---")
    for k in range(rec_idx - 15, rec_idx + 10):
        rec = doc0.records[k]
        tag = rec['tag']
        txt = rec['payload'].decode('utf-16le', errors='ignore') if tag in (2201, 2202) else ''
        extra = ""
        if tag == 2100 and len(rec['payload']) >= 12:
            mat = struct.unpack('<iii', rec['payload'][:12])
            x_cm = mat[0] * 2.54 / 72000
            extra = f"X={x_cm:.4f}cm (mp={mat[0]})"
        elif tag == 2206 and len(rec['payload']) >= 12:
            adv = struct.unpack('<iii', rec['payload'][:12])
            extra = f"adv={adv}"
        print(f"  Rec {k:5d}: Tag {tag:4d} | txt='{txt}' | {extra}")
