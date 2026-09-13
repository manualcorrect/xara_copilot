import os
from xar_dom_engine import XarDocument

def execute_tahap3():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap2.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap3.xar'

    print("=========================================================================")
    print("   PROJECT V2: TAHAP 3 - PERUBAHAN TANGGAL CETAK (10 Sep 2026)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Total records loaded: {total_recs_before}")

    # Updates for Page 1 & Page 2
    # Rec 964 & 3668: '1'
    # Rec 968 & 3672: '0'
    # Rec 976 & 3680: 'Sep '
    # Rec 981 & 3685: '2026'

    p1_nodes = [(964, "1"), (968, "0"), (976, "Sep "), (981, "2026")]
    p2_nodes = [(3668, "1"), (3672, "0"), (3680, "Sep "), (3685, "2026")]

    for page_num, nodes in [(1, p1_nodes), (2, p2_nodes)]:
        for rec_idx, val in nodes:
            old_val = doc.records[rec_idx]['payload'].decode('utf-16le', errors='ignore')
            new_payload = bytearray(val.encode('utf-16le'))
            doc.records[rec_idx]['payload'] = new_payload
            doc.records[rec_idx]['size'] = len(new_payload)
            print(f"[*] Page {page_num}: Rec {rec_idx:05d} updated from {repr(old_val)} -> {repr(val)}")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 3 completed! Saved to {out_path}")
    print(f"[*] Records verification: {total_recs_after} records (Zero-shift maintained: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap3()
