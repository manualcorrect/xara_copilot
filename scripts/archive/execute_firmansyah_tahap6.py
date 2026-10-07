import os
from xar_dom_engine import XarDocument

def execute_tahap6():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap5.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap6.xar'

    print("=========================================================================")
    print("   PROJECT V2: TAHAP 6 - PERUBAHAN TANGGAL & TIMESTAMP JAM (22 BARIS)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Total records loaded: {total_recs_before}")

    # Row Date Updates:
    # (row_num, [(rec_idx, new_text), ...])
    date_updates = [
        (1, [(1562, "01"), (1567, "Jun 2026")]),
        (2, [(1702, "01 Jun 2026")]),
        (3, [(1875, "02 Jun 2026")]),
        (4, [(2036, "02 Jun 2026")]),
        (5, [(2202, "03 Jun 2026")]),
        (6, [(2381, "04 Jun 2026")]),
        (7, [(2547, "04 Jun 2026")]),
        (8, [(2682, "05 Jun 2026")]),
        (9, [(2845, "05 Jun 2026")]),
        (10, [(2963, "06 Jun 2026")]),
        (11, [(4109, "07 Jun 2026")]),
        (12, [(4249, "08 Jun 2026")]),
        (13, [(4389, "08 Jun 2026")]),
        (14, [(4519, "09 Jun 2026")]),
        (15, [(4674, "10 Jun 2026")]),
        (16, [(4814, "11 Jun 2026")]),
        (17, [(4949, "12 Jun 2026")]),
        (18, [(5084, "13 Jun 2026")]),
        (19, [(5241, "14 Jun 2026")]),
        (20, [(5388, "15 Jun 2026")]),
        (21, [(5538, "1"), (5542, "5"), (5550, "Jun 2026")]),
        (22, [(5654, "1"), (5658, "5"), (5666, "Jun 2026")])
    ]

    for r_num, updates in date_updates:
        for rec_idx, val in updates:
            old_val = doc.records[rec_idx]['payload'].decode('utf-16le', errors='ignore')
            new_payload = bytearray(val.encode('utf-16le'))
            doc.records[rec_idx]['payload'] = new_payload
            doc.records[rec_idx]['size'] = len(new_payload)
            print(f"[*] Row {r_num:02d} Date: Rec {rec_idx:05d} {repr(old_val)} -> {repr(val)}")

    # Row Time Updates:
    time_updates = [
        (1, [(1537, "04:00:00 W"), (1542, "IB")]),
        (2, [(1677, "04:12:1"), (1682, "5 WIB")]),
        (3, [(1850, "08:30:0"), (1855, "0 WIB")]),
        (4, [(2011, "09:15:22 "), (2016, "WIB")]),
        (5, [(2182, "10:05:10 WIB")]),
        (6, [(2361, "11:20:45 WIB")]),
        (7, [(2522, "12:00:0"), (2527, "0 WIB")]),
        (8, [(2657, "13:45:12 WI"), (2662, "B")]),
        (9, [(2820, "14:10:00 WI"), (2825, "B")]),
        (10, [(2943, "15:25:30 WIB")]),
        (11, [(4089, "07:10:05 WIB")]),
        (12, [(4224, "08:50:1"), (4229, "1 WIB")]),
        (13, [(4364, "09:30:0"), (4369, "0 WIB")]),
        (14, [(4494, "10:00:0"), (4499, "0 WIB")]),
        (15, [(4654, "11:15:20 WIB")]),
        (16, [(4789, "12:35:40 W"), (4794, "IB")]),
        (17, [(4924, "13:10:00 W"), (4929, "IB")]),
        (18, [(5059, "14:20:15 WI"), (5064, "B")]),
        (19, [(5216, "15:05:00 WI"), (5221, "B")]),
        (20, [(5368, "09:00:00 WIB")]),
        (21, [(5513, "10:45:10 WIB")]),
        (22, [(5629, "11:12:00 WIB")])
    ]

    for r_num, updates in time_updates:
        for rec_idx, val in updates:
            old_val = doc.records[rec_idx]['payload'].decode('utf-16le', errors='ignore')
            new_payload = bytearray(val.encode('utf-16le'))
            doc.records[rec_idx]['payload'] = new_payload
            doc.records[rec_idx]['size'] = len(new_payload)
            print(f"[*] Row {r_num:02d} Time: Rec {rec_idx:05d} {repr(old_val)} -> {repr(val)}")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 6 completed! Saved to {out_path}")
    print(f"[*] Records verification: {total_recs_after} records (Zero-shift maintained: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap6()
