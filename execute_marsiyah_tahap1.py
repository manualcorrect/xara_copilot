import os
import sys
import struct
from xar_dom_engine import XarDocument

def execute_tahap1():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap1.xar'

    print("=========================================================================")
    print("   PROJECT V2 TRAINING: TAHAP 1 - PERUBAHAN NAMA NASABAH")
    print("   Target Dokumen: 7 Halaman (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Dokumen dimuat: {total_recs_before:,} records")

    NEW_NAME = "MASRIYAH MUHAMMAD SAMIAN "
    name_payload = bytearray(NEW_NAME.encode('utf-16le'))
    name_size = len(name_payload)

    targets = [
        (1, 985, 986),
        (2, 3569, 3570),
        (3, 6312, 6313),
        (4, 9054, 9055),
        (5, 11809, 11810),
        (6, 14563, 14564),
        (7, 17430, 17431)
    ]

    for page_num, kern_idx, name_idx in targets:
        old_text = doc.records[name_idx]['payload'].decode('utf-16le', errors='ignore')
        assert 'ROY DARWIN' in old_text, f"Verifikasi gagal pada Page {page_num}! Ditemukan: {old_text}"

        # Update Name Payload
        doc.records[name_idx]['payload'] = name_payload
        doc.records[name_idx]['size'] = name_size

        # In 0.xar Tag 2206 width:
        w_old, h_old, flags_old = struct.unpack('<iii', doc.records[kern_idx]['payload'][:12])
        # Scale advance width proportional to length or preserve
        new_w = int(w_old * (len(NEW_NAME) / len(old_text)))
        doc.records[kern_idx]['payload'] = bytearray(struct.pack('<iii', new_w, h_old, flags_old))
        doc.records[kern_idx]['size'] = len(doc.records[kern_idx]['payload'])

        print(f"[*] Page {page_num}: Record {name_idx:05d} updated from {repr(old_text)} -> {repr(NEW_NAME)} (Tag 2206 Width: {w_old} -> {new_w})")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 1 Selesai 100%! Output tersimpan di: {out_path}")
    print(f"[*] Zero-Shift Check: {total_recs_before:,} -> {total_recs_after:,} (Status: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap1()
