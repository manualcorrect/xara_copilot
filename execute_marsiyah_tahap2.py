import os
import sys
from xar_dom_engine import XarDocument

def execute_tahap2():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap1.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap2.xar'

    print("=========================================================================")
    print("   PROJECT V2 TRAINING: TAHAP 2 - PERUBAHAN PERIODE LAPORAN")
    print("   Target Dokumen: 7 Halaman (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Dokumen dimuat: {total_recs_before:,} records")

    NEW_PERIOD_PART = "Jun 2026 - 30 Jun 2026"
    period_payload = bytearray(NEW_PERIOD_PART.encode('utf-16le'))
    period_size = len(period_payload)

    target_period_recs = [
        (1, 1019, 1023, 1031),
        (2, 3603, 3607, 3615),
        (3, 6346, 6350, 6358),
        (4, 9088, 9092, 9100),
        (5, 11843, 11847, 11855),
        (6, 14597, 14601, 14609),
        (7, 17464, 17468, 17476)
    ]

    for p, d1, d2, p_rec in target_period_recs:
        old_text = doc.records[p_rec]['payload'].decode('utf-16le', errors='ignore')
        assert 'Jan 2026' in old_text, f"Verifikasi gagal pada Page {p}! Ditemukan: {old_text}"

        # Day digits 01 are already '0' and '1'
        doc.records[d1]['payload'] = bytearray('0'.encode('utf-16le'))
        doc.records[d1]['size'] = 2
        doc.records[d2]['payload'] = bytearray('1'.encode('utf-16le'))
        doc.records[d2]['size'] = 2

        doc.records[p_rec]['payload'] = period_payload
        doc.records[p_rec]['size'] = period_size

        print(f"[*] Page {p}: Periode Rec {p_rec:05d} updated from '01 {old_text}' -> '01 {NEW_PERIOD_PART}'")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 2 Selesai 100%! Output tersimpan di: {out_path}")
    print(f"[*] Zero-Shift Check: {total_recs_before:,} -> {total_recs_after:,} (Status: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap2()
