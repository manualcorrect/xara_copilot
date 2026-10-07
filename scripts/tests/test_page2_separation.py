import struct
from xar_dom_engine import XarDocument

def apply_page2_separation():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    # 1. Extract Page 5 Cabang object slice (30 records: Rec 14064 to 14093)
    cabang_slice = []
    for r in range(14064, 14094):
        rec = doc.records[r]
        cabang_slice.append({
            'tag': rec['tag'],
            'size': rec['size'],
            'payload': bytearray(rec['payload'])
        })
    print(f"[*] Extracted Cabang object slice from Page 5: {len(cabang_slice)} records")

    # 2. Modify Page 2 Nama Story (Rec 3626 to 3635)
    # Line 1: MASRIYAH MUHAMMAD 
    doc.records[3628]['payload'] = bytearray.fromhex('8a5d01008116000000000000') # w=89482 mp, dy=0
    doc.records[3628]['size'] = 12

    name1_str = "MASRIYAH MUHAMMAD "
    name1_payload = bytearray(name1_str.encode('utf-16le'))
    doc.records[3629]['payload'] = name1_payload
    doc.records[3629]['size'] = len(name1_payload)

    # Line 2: SAMIAN  (with 10pt leading = -10,000 mp)
    doc.records[3633]['payload'] = bytearray.fromhex('f178000081160000f0d8ffff') # w=30961 mp, dy=-10000 mp
    doc.records[3633]['size'] = 12

    name2_str = "SAMIAN "
    name2_payload = bytearray(name2_str.encode('utf-16le'))
    doc.records[3634]['payload'] = name2_payload
    doc.records[3634]['size'] = len(name2_payload)

    print(f"[*] Page 2 Nama Story updated: Line 1='{name1_str}', Line 2='{name2_str}' (10pt leading)")

    # 3. Find insertion point for Page 2 Cabang object (between Rec 5867 and Rec 5868)
    insert_pos = 5868
    print(f"[*] Inserting Cabang object on Page 2 at index {insert_pos}...")
    for idx, item in enumerate(cabang_slice):
        doc.records.insert(insert_pos + idx, item)

    # 4. Sync record sizes & save
    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Page 2 Nama & Cabang separation applied! Total records: {len(doc.records):,}")

if __name__ == '__main__':
    apply_page2_separation()
