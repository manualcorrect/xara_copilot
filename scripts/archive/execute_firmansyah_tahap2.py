import os
from xar_dom_engine import XarDocument

def execute_tahap2():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap1.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap2.xar'

    print("=========================================================================")
    print("   PROJECT V2: TAHAP 2 - PERUBAHAN PERIODE (01 Jun 2026 - 30 Jun 2026)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Total records loaded: {total_recs_before}")

    new_period_suffix = "Jun 2026 - 30 Jun 2026"
    new_payload = bytearray(new_period_suffix.encode('utf-16le'))

    # Page 1: Rec 952
    old_p1 = doc.records[952]['payload'].decode('utf-16le', errors='ignore')
    doc.records[952]['payload'] = new_payload
    doc.records[952]['size'] = len(new_payload)
    print(f"[*] Page 1: Rec 00952 updated from {repr(old_p1)} -> {repr(new_period_suffix)}")

    # Page 2: Rec 3656
    old_p2 = doc.records[3656]['payload'].decode('utf-16le', errors='ignore')
    doc.records[3656]['payload'] = new_payload
    doc.records[3656]['size'] = len(new_payload)
    print(f"[*] Page 2: Rec 03656 updated from {repr(old_p2)} -> {repr(new_period_suffix)}")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 2 completed! Saved to {out_path}")
    print(f"[*] Records verification: {total_recs_after} records (Zero-shift maintained: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap2()
