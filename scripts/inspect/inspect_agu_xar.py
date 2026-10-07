from xar_dom_engine import XarDocument

agu_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar'
doc = XarDocument(agu_xar)
print(f"Total records in Agu 0.xar: {len(doc.records):,}")

# Find total pages (Tag 2000, 2001, or page definitions)
page_tags = [i for i, r in enumerate(doc.records) if r['tag'] in (2000, 2001, 2002, 2003, 2004, 2005)]
print(f"Page definition records: {len(page_tags)}")

# Inspect text records
texts = []
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if txt.strip():
                texts.append((i, r['tag'], txt))
        except:
            pass

print(f"Total non-empty text records: {len(texts):,}")

print("\n--- Header Search (FIRMANSYAH / YULIANA / Nama) ---")
for i, tag, txt in texts:
    if any(w in txt.upper() for w in ['FIRMANSYAH', 'YULIANA', 'SANI', 'PUTRI', 'BENDI', 'AUG', 'AGU', 'JUL', 'OF ', 'DARI ']):
        print(f"Rec {i:5d} (Tag {tag}): '{txt}'")

print("\n--- Account & Summary Search ---")
for i, tag, txt in texts:
    if any(w in txt for w in ['1630', '163', '1094', '5.891', '10.165', '9.618', '6.438', '1.929', '14000']):
        print(f"Rec {i:5d} (Tag {tag}): '{txt}'")

print("\n--- Sample Table Row Numbers (e.g. 1..10, 20..30) ---")
for i, tag, txt in texts:
    if txt.strip() in [str(n) for n in range(1, 35)]:
        print(f"Rec {i:5d} (Tag {tag}): '{txt}'")
