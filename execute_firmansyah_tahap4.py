import os
from xar_dom_engine import XarDocument

def execute_tahap4():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap3.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap4.xar'

    print("=========================================================================")
    print("   PROJECT V2: TAHAP 4 - PERUBAHAN NOMOR REKENING (1630010942426)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Total records loaded: {total_recs_before}")

    part1 = "16300109424"
    part2 = "26 "

    old_p1 = doc.records[1002]['payload'].decode('utf-16le', errors='ignore')
    old_p2 = doc.records[1007]['payload'].decode('utf-16le', errors='ignore')

    payload1 = bytearray(part1.encode('utf-16le'))
    payload2 = bytearray(part2.encode('utf-16le'))

    doc.records[1002]['payload'] = payload1
    doc.records[1002]['size'] = len(payload1)

    doc.records[1007]['payload'] = payload2
    doc.records[1007]['size'] = len(payload2)

    print(f"[*] Rec 01002: {repr(old_p1)} -> {repr(part1)}")
    print(f"[*] Rec 01007: {repr(old_p2)} -> {repr(part2)}")
    print(f"[*] Full Account Number: '{part1}{part2}'")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 4 completed! Saved to {out_path}")
    print(f"[*] Records verification: {total_recs_after} records (Zero-shift maintained: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap4()
