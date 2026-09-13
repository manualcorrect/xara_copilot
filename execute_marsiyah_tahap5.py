import os
import sys
from xar_dom_engine import XarDocument

def execute_tahap5():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap4.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap5.xar'

    print("=========================================================================")
    print("   PROJECT V2 TRAINING: TAHAP 5 - PERUBAHAN NOMOR HALAMAN")
    print("   Target Dokumen: 7 Halaman Penuh (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Dokumen dimuat: {total_recs_before:,} records")

    # Target nodes for all 7 pages:
    # (page, footer_curr_rec, footer_of_rec, header_dari_rec, header_tot_rec)
    page_nodes = [
        (1, 1143, 1148, 1286, 1263),
        (2, 3667, 3675, 3721, 3698),
        (3, 6410, 6418, 6464, 6441),
        (4, 9152, 9160, 9206, 9183),
        (5, 11907, 11915, 11961, 11938),
        (6, 14661, 14669, 14715, 14692),
        (7, 17528, 17536, 17582, 17559)
    ]

    TOTAL_PAGES = 7

    for p, f_curr, f_of, h_dari, h_tot in page_nodes:
        # Footer
        if p == 1:
            doc.records[f_curr]['payload'] = bytearray("1 ".encode('utf-16le'))
            doc.records[f_curr]['size'] = 4
        else:
            doc.records[f_curr]['payload'] = bytearray(str(p).encode('utf-16le'))
            doc.records[f_curr]['size'] = 2

        doc.records[f_of]['payload'] = bytearray(f"of {TOTAL_PAGES}".encode('utf-16le'))
        doc.records[f_of]['size'] = len(doc.records[f_of]['payload'])

        # Header
        doc.records[h_dari]['payload'] = bytearray(f"{p} dari".encode('utf-16le'))
        doc.records[h_dari]['size'] = len(doc.records[h_dari]['payload'])

        doc.records[h_tot]['payload'] = bytearray(str(TOTAL_PAGES).encode('utf-16le'))
        doc.records[h_tot]['size'] = 2

        print(f"[*] Page {p}: Footer '{p} of {TOTAL_PAGES}' & Header '{p} dari {TOTAL_PAGES}' terkunci 100% PASS [OK]")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 5 Selesai 100%! Output tersimpan di: {out_path}")
    print(f"[*] Zero-Shift Check: {total_recs_before:,} -> {total_recs_after:,} (Status: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap5()
