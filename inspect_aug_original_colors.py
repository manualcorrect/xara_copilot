from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar')

print("=== ORIGINAL COLORS IN AUG/0.XAR ===")

# Credit nominals
print("\n--- CREDIT NOMINALS (+) ---")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if txt.startswith('+'):
            col = None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 150:
                    col = doc.records[k]['payload'].hex()
            print(f"Rec {i:5d} ({txt!r}): Color = {col}")

# Debit nominals
print("\n--- DEBIT NOMINALS (-) (first 3) ---")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if txt.startswith('-'):
            col = None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 150:
                    col = doc.records[k]['payload'].hex()
            print(f"Rec {i:5d} ({txt!r}): Color = {col}")
            if i > 2500:
                break

# Saldo
print("\n--- SALDO (first 3) ---")
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if txt.endswith(',81') and '.' in txt and len(txt) > 5 and not txt.startswith('+') and not txt.startswith('-'):
            col = None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 150:
                    col = doc.records[k]['payload'].hex()
            print(f"Rec {i:5d} ({txt!r}): Color = {col}")
            if i > 2500:
                break
