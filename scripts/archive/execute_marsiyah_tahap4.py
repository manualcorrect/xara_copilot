import os
import sys
from xar_dom_engine import XarDocument

def execute_tahap4():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap3.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap4.xar'

    print("=========================================================================")
    print("   PROJECT V2 TRAINING: TAHAP 4 - PERUBAHAN NOMOR REKENING")
    print("   Target Dokumen: Header Page 1 (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Dokumen dimuat: {total_recs_before:,} records")

    NEW_ACC = "1630016144514 "
    acc_payload = bytearray(NEW_ACC.encode('utf-16le'))
    acc_size = len(acc_payload)

    acc_rec = 1078
    old_acc = doc.records[acc_rec]['payload'].decode('utf-16le', errors='ignore')
    assert '1650003584860' in old_acc, f"Verifikasi gagal pada Rec {acc_rec}! Ditemukan: {old_acc}"

    doc.records[acc_rec]['payload'] = acc_payload
    doc.records[acc_rec]['size'] = acc_size

    print(f"[*] Page 1: Nomor Rekening Rec {acc_rec:05d} updated from {repr(old_acc)} -> {repr(NEW_ACC)}")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 4 Selesai 100%! Output tersimpan di: {out_path}")
    print(f"[*] Zero-Shift Check: {total_recs_before:,} -> {total_recs_after:,} (Status: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap4()
