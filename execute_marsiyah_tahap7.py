import os
import sys
import struct
from xar_dom_engine import XarDocument

def execute_tahap7():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap6.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap7.xar'

    print("=========================================================================")
    print("   PROJECT V2 TRAINING: TAHAP 7 - PERUBAHAN RINGKASAN & TABEL TRANSAKSI (FINAL)")
    print("   Target Dokumen: 7 Halaman / 73 Baris Penuh (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Dokumen dimuat: {total_recs_before:,} records")

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

    # 1. Update Financial Summary Header
    # Dana Masuk: Rec 1182 ('+ 11.055.000,00'), Rec 1187 (blank)
    update_text(1182, "+ 11.055.000,00")
    blank_node(1187)
    update_color(1178, COLOR_GREEN)
    update_t2206(1177, 65000)

    # Dana Keluar: Rec 1199 ('- 5.123.603,00 ')
    update_text(1199, "- 5.123.603,00 ")
    update_color(1193, COLOR_BLACK)
    update_t2206(1192, 65000)

    # Saldo Akhir: Rec 1211 ('6.377.347,81')
    update_text(1211, "6.377.347,81")
    update_color(1205, COLOR_BLUE)
    update_t2206(1203, 43894)

    print("[*] Financial Summary Header updated: Masuk='+ 11.055.000,00', Keluar='- 5.123.603,00', Akhir='6.377.347,81'")

    # 2. Update Row 56 (Deposit + 6.355.000,00)
    # Nominal: Rec 13620 -> '+ 6.355.000,00'
    update_text(13620, "+ 6.355.000,00")
    update_color(13606, COLOR_GREEN)
    update_t2206(13619, 61061)

    # Saldo: Rec 13587 -> '6.502.335,81'
    update_text(13587, "6.502.335,81")
    print("[*] Row 56 updated: Nominal='+ 6.355.000,00' (Green CR), Saldo='6.502.335,81'")

    # 3. Update Running Saldos for Rows 57 to 73
    new_saldos = {
        57: (13739, "6.465.335,81"),
        58: (13889, "6.715.335,81"),
        59: (14989, "6.650.347,81"),
        60: (15134, "6.649.347,81"),
        61: (15274, "6.613.347,81"),
        62: (15442, "6.583.347,81"),
        63: (15603, "6.383.347,81"),
        64: (15758, "6.483.347,81"),
        65: (15908, "6.482.347,81"),
        66: (16048, "6.382.347,81"),
        67: (16215, "6.682.347,81"),
        68: (16374, "6.482.347,81"),
        69: (16546, "6.582.347,81"),
        70: (16713, "6.382.347,81"),
        71: (17869, "6.582.347,81"),
        72: (18021, "6.382.347,81"),
        73: (18161, "6.377.347,81")
    }

    for r_num, (rec_idx, sal_str) in sorted(new_saldos.items()):
        old_val = doc.records[rec_idx]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        update_text(rec_idx, sal_str)
        if r_num in (57, 63, 70, 73):
            print(f"[*] Row {r_num:2d}: Saldo Rec {rec_idx} updated from '{old_val}' -> '{sal_str}'")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Post-Flight Integrity Gate: Zero-Shift Check
    total_recs_after = len(doc.records)
    assert total_recs_before == total_recs_after, f"Zero-shift violation! Before {total_recs_before} != After {total_recs_after}"

    # Post-Flight Gate: No 0-byte Tag 2201/2202 nodes
    zero_nodes = [i for i, r in enumerate(doc.records) if r['tag'] in (2201, 2202) and r['size'] == 0]
    assert len(zero_nodes) == 0, f"Found 0-byte text nodes: {zero_nodes}"

    # Save final Tahap 7 output
    doc.save(out_path)
    print(f"\n[SUCCESS] Tahap 7 (FINAL) Selesai 100%! Output tersimpan di: {out_path}")
    print(f"[*] Zero-Shift Check: {total_recs_before:,} -> {total_recs_after:,} (100% Locked)")
    print(f"[*] Post-Flight Integrity Gates: 100% PASS [OK]")

if __name__ == '__main__':
    execute_tahap7()
