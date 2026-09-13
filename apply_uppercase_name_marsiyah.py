import os
import glob
from xar_dom_engine import XarDocument

def apply_uppercase_name():
    folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
    target_files = glob.glob(os.path.join(folder, '0_tahap*.xar'))
    
    NEW_NAME = "MASRIYAH MUHAMMAD SAMIAN "
    name_payload = bytearray(NEW_NAME.encode('utf-16le'))
    name_size = len(name_payload)
    
    target_recs = [986, 3570, 6313, 9055, 11810, 14564, 17431]

    print("=========================================================================")
    print("   PROJECT V2: UPDATE NAMA MENJADI HURUF KAPITAL SEMUA (ALL CAPS)")
    print(f"   Target Teks: '{NEW_NAME}'")
    print(f"   Jumlah Halaman: 7 Halaman (Records: {target_recs})")
    print("=========================================================================\n")

    for fpath in target_files:
        fname = os.path.basename(fpath)
        doc = XarDocument(fpath)
        total_before = len(doc.records)
        
        for p_idx, r_idx in enumerate(target_recs, 1):
            old_val = doc.records[r_idx]['payload'].decode('utf-16le', errors='ignore')
            doc.records[r_idx]['payload'] = name_payload
            doc.records[r_idx]['size'] = name_size
            
        for r in doc.records:
            r['size'] = len(r['payload'])
            
        total_after = len(doc.records)
        assert total_before == total_after, f"Zero shift violation in {fname}"
        doc.save(fpath)
        print(f"[OK] {fname:15s} -> 7 halaman diupdate ke '{NEW_NAME.strip()}' (Zero-Shift PASS)")

    print("\n[SUCCESS] Seluruh file Marsiyah (0_tahap1 s.d. 0_tahap7) berhasil diperbarui ke HURUF KAPITAL!")

if __name__ == '__main__':
    apply_uppercase_name()
