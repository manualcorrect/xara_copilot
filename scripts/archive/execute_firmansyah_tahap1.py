import os
import struct
from xar_dom_engine import XarDocument

def execute_tahap1():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jun\0_tahap1.xar'

    print("=========================================================================")
    print("   PROJECT V2: TAHAP 1 - PERUBAHAN NAMA NASABAH (FIRMANSYAH)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Total records loaded: {total_recs_before}")

    # Inspect font metrics for 'EHA JULAEHA '
    for kern_idx, name_idx, page in [(898, 899, 1), (3602, 3603, 2)]:
        r_kern = doc.records[kern_idx]
        w, h, flags = struct.unpack('<iii', r_kern['payload'][:12])
        old_name = doc.records[name_idx]['payload'].decode('utf-16le', errors='ignore')
        print(f"[*] Page {page}: Name Rec {name_idx} = {repr(old_name)}, Kern Rec {kern_idx} = w:{w}, h:{h}, flags:{flags}")

    # Calculate advance width for FIRMANSYAH
    # TTInterphases-Regular glyph widths:
    # F: 4620, I: 2200, R: 5040, M: 7140, A: 5040, N: 5500, S: 4620, Y: 4620, A: 5040, H: 5500, space: 2200
    # Let's inspect character widths table in calc_char_widths.py
    new_name_str = "FIRMANSYAH "
    name_payload = bytearray(new_name_str.encode('utf-16le'))

    # Update Page 1 and Page 2
    for kern_idx, name_idx, page in [(898, 899, 1), (3602, 3603, 2)]:
        old_text = doc.records[name_idx]['payload'].decode('utf-16le', errors='ignore')
        doc.records[name_idx]['payload'] = name_payload
        doc.records[name_idx]['size'] = len(name_payload)

        # In 0.xar, kerning Tag 2206 w was 0 for Rec 898 and 3602
        # Let's preserve h and flags
        w, h, flags = struct.unpack('<iii', doc.records[kern_idx]['payload'][:12])
        doc.records[kern_idx]['size'] = len(doc.records[kern_idx]['payload'])
        print(f"[*] Page {page}: Record {name_idx} updated from {repr(old_text)} -> {repr(new_name_str)}")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 1 completed! Saved to {out_path}")
    print(f"[*] Records verification: {total_recs_after} records (Zero-shift maintained: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap1()
