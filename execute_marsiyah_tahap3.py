import os
import sys
from xar_dom_engine import XarDocument

def execute_tahap3():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap2.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap3.xar'

    print("=========================================================================")
    print("   PROJECT V2 TRAINING: TAHAP 3 - PERUBAHAN TANGGAL CETAK")
    print("   Target Dokumen: 7 Halaman (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Dokumen dimuat: {total_recs_before:,} records")

    # New Date: '10 Sep 2026'
    # d1 = '1', d2 = '0', my = 'Sep 2026'
    b_d1 = bytearray('1'.encode('utf-16le'))
    b_d2 = bytearray('0'.encode('utf-16le'))
    b_my = bytearray('Sep 2026'.encode('utf-16le'))

    targets = [
        (1, 1043, 1047, 1055),
        (2, 3627, 3631, 3639),
        (3, 6370, 6374, 6382),
        (4, 9112, 9116, 9124),
        (5, 11867, 11871, 11879),
        (6, 14621, 14625, 14633),
        (7, 17488, 17492, 17500)
    ]

    for p, d1, d2, my in targets:
        old_d1 = doc.records[d1]['payload'].decode('utf-16le')
        old_d2 = doc.records[d2]['payload'].decode('utf-16le')
        old_my = doc.records[my]['payload'].decode('utf-16le')

        doc.records[d1]['payload'] = b_d1
        doc.records[d1]['size'] = 2

        doc.records[d2]['payload'] = b_d2
        doc.records[d2]['size'] = 2

        doc.records[my]['payload'] = b_my
        doc.records[my]['size'] = len(b_my)

        print(f"[*] Page {p}: Dicetak Pada updated from '{old_d1}{old_d2} {old_my}' -> '10 Sep 2026'")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 3 Selesai 100%! Output tersimpan di: {out_path}")
    print(f"[*] Zero-Shift Check: {total_recs_before:,} -> {total_recs_after:,} (Status: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap3()
