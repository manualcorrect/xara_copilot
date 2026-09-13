import os
import sys
import struct
from xar_dom_engine import XarDocument

def apply_perfect_fix():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap6.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar'

    print("=========================================================================")
    print("   PROJECT V2: MARSIYAH TAHAP 7 - PERFECT ALIGNMENT & CONSISTENCY FIX")
    print("   Target: 7 Halaman / 73 Baris Penuh (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)

    # Native Colors for this 7-page document profile
    COLOR_GREEN = bytearray.fromhex('d6030000') # Native Green (Dana Masuk / Kredit)
    COLOR_BLACK = bytearray.fromhex('9d010000') # Native Black (Dana Keluar / Debit)
    COLOR_BLUE  = bytearray.fromhex('28050000') # Native Blue (Saldo Akhir / Running Saldo)
    COLOR_GRAY  = bytearray.fromhex('72030000') # Native Dark Gray (Saldo Awal)

    def update_text(rec_idx, text_str):
        p = bytearray(text_str.encode('utf-16le'))
        doc.records[rec_idx]['payload'] = p
        doc.records[rec_idx]['size'] = len(p)

    def blank_node(rec_idx):
        doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
        doc.records[rec_idx]['size'] = 2

    def update_color(rec_idx, color_bytes):
        doc.records[rec_idx]['payload'] = color_bytes
        doc.records[rec_idx]['size'] = len(color_bytes)

    def update_t2206(rec_idx, new_w):
        orig = struct.unpack('<iii', doc.records[rec_idx]['payload'][:12])
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_w, orig[1], orig[2]))
        doc.records[rec_idx]['size'] = 12

    def update_t2100(rec_idx, new_x, new_y):
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', new_x, new_y, 1))
        doc.records[rec_idx]['size'] = 12

    def update_t2204(rec_idx, new_dx, new_dy):
        doc.records[rec_idx]['payload'] = bytearray(struct.pack('<ii', new_dx, new_dy))
        doc.records[rec_idx]['size'] = 8

    # 1. Update Financial Summary Header
    update_text(1182, "+ 11.055.000,00")
    blank_node(1187)
    update_color(1178, COLOR_GREEN)
    update_t2206(1177, 65000)

    update_text(1199, "- 5.123.603,00 ")
    update_color(1193, COLOR_BLACK)
    update_t2206(1192, 65000)

    update_text(1211, "6.377.347,81")
    update_color(1205, COLOR_BLUE)
    update_t2206(1203, 43894)

    # 2. Fix Chronological Times on 25 Jun 2026 (Rows 56, 57, 58)
    update_text(13642, "08:39:33 WIB") # Row 56
    update_text(13799, "10:15:30 WIB") # Row 57
    update_text(13949, "12:56:29 WIB") # Row 58

    # 3. Fix Row 56 Description (Transfer Masuk / Deposit)
    update_text(13541, "Transfer antar Mandiri ")
    update_text(13546, "DARI PT BENDI NASHA NIAGA ")
    update_text(13551, "INDUSTRI 1630010942426 ")
    update_text(13556, "Transfer")

    # 4. Fix Row 56 Nominal (+6.355.000,00 without space, Tag 2100 & Tag 2206 right-aligned)
    update_text(13620, "+6.355.000,00")
    update_color(13606, COLOR_GREEN)
    update_t2100(13601, 373800, 194000)
    update_t2206(13619, 57601)

    # 5. Fix Saldo and Tag 2204 Right-Alignment for Rows 56 to 73
    new_saldos = {
        56: (13587, "6.502.335,81", 13581, 62200, 4478400),
        57: (13739, "6.465.335,81", 13733, 62195, 4478040),
        58: (13889, "6.715.335,81", 13883, 61985, 4462920),
        59: (14989, "6.650.347,81", 14983, 62060, 4468320),
        60: (15134, "6.649.347,81", 15128, 61975, 4462200),
        61: (15274, "6.613.347,81", 15268, 62380, 4491360),
        62: (15442, "6.583.347,81", 15436, 62160, 4475520),
        63: (15603, "6.383.347,81", 15597, 62445, 4496040),
        64: (15758, "6.483.347,81", 15752, 62370, 4490640),
        65: (15908, "6.482.347,81", 15902, 62275, 4483800),
        66: (16048, "6.382.347,81", 16042, 62365, 4490280),
        67: (16215, "6.682.347,81", 16209, 62130, 4473360),
        68: (16374, "6.482.347,81", 16368, 62265, 4483080),
        69: (16546, "6.582.347,81", 16540, 62075, 4469400),
        70: (16713, "6.382.347,81", 16707, 62340, 4488480),
        71: (17869, "6.582.347,81", 17863, 62385, 4491720),
        72: (18021, "6.382.347,81", 18015, 62445, 4496040),
        73: (18161, "6.377.347,81", 18155, 62655, 4511160)
    }

    for r_num, (s_rec, s_val, k_rec, new_dx, new_dy) in sorted(new_saldos.items()):
        update_text(s_rec, s_val)
        update_t2204(k_rec, new_dx, new_dy)

    # Auto-sync all record sizes
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Post-Flight Integrity Gate: Zero-Shift Check
    total_recs_after = len(doc.records)
    assert total_recs_before == total_recs_after, f"Zero-shift violation! Before {total_recs_before} != After {total_recs_after}"

    # Post-Flight Gate: No 0-byte Tag 2201/2202 nodes
    zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
    assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"

    # Save output
    doc.save(out_path)
    print(f"[SUCCESS] Marsiyah Tahap 7 Berhasil Diperbarui 100%! Output: {out_path}")

if __name__ == '__main__':
    apply_perfect_fix()
