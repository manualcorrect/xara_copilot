from xar_dom_engine import XarDocument

agu_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar'
doc = XarDocument(agu_xar)

# Search Dana Masuk
print("=== DANA MASUK SEARCH ===")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(w in txt for w in ['12.964', '12.9', '+ 12', '+12']):
                print(f"Rec {i:5d} (Tag {r['tag']}): '{txt}'")
        except:
            pass

# Search Table Rows: find where the transactions are
print("\n=== SAMPLE TRANSACTION AMOUNTS IN AGU ===")
sample_amts = ['13.000', '130.000', '1.000.000', '50.000', '250.000', '500.000', '1.200.000', '2.000.000', '10.000', '25.000']
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(a in txt for a in sample_amts):
                print(f"Rec {i:5d} (Tag {r['tag']}): '{txt}'")
        except:
            pass
