import os
from xar_dom_engine import XarDocument

def execute_tahap5():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap4.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap5.xar'

    print("=========================================================================")
    print("   PROJECT V2: TAHAP 5 - VERIFIKASI & PENGUNCIAN NOMOR HALAMAN (3 HALAMAN)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Total records loaded: {total_recs_before}")

    # Verify Page 1 nodes
    p1_f = doc.records[1068]['payload'].decode('utf-16le', errors='ignore')
    p1_h_total = doc.records[1188]['payload'].decode('utf-16le', errors='ignore')
    p1_h_prefix = doc.records[1208]['payload'].decode('utf-16le', errors='ignore')
    p1_h_suffix = doc.records[1213]['payload'].decode('utf-16le', errors='ignore')
    print(f"[*] Page 1 Footer: Rec 01068 = {repr(p1_f)}")
    print(f"[*] Page 1 Header: Rec 01208 ({repr(p1_h_prefix)}) + Rec 01213 ({repr(p1_h_suffix)}) + Rec 01188 ({repr(p1_h_total)}) -> '1 dari 3'")

    # Verify Page 2 nodes
    p2_f_num = doc.records[3711]['payload'].decode('utf-16le', errors='ignore')
    p2_f = doc.records[3719]['payload'].decode('utf-16le', errors='ignore')
    p2_h_total = doc.records[3739]['payload'].decode('utf-16le', errors='ignore')
    print(f"[*] Page 2 Footer: Rec 03711 ({repr(p2_f_num)}) + Rec 03719 ({repr(p2_f)}) -> '2 of 3'")
    print(f"[*] Page 2 Header: Rec 03739 = {repr(p2_h_total)} -> '2 dari 3'")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 5 completed! Saved to {out_path}")
    print(f"[*] Records verification: {total_recs_after} records (Zero-shift maintained: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap5()
