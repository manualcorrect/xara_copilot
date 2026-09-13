from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Let's inspect all text nodes around nominal and saldo for all 22 rows in original 0.xar
nom_recs = [1587, 1778, 1949, 2115, 2316, 2477, 2643, 2823, 3014, 3192,
            4215, 4401, 4587, 4753, 4929, 5114, 5300, 5471, 5632, 5808, 5994, 6160]

for idx, n_idx in enumerate(nom_recs, 1):
    print(f"\n==================== ROW {idx} ====================")
    # Print all text nodes from n_idx to n_idx + 45
    for j in range(n_idx, min(len(doc.records), n_idx + 45)):
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            print(f"  Rec {j:4d} | Tag {r['tag']} | {repr(txt)}")
