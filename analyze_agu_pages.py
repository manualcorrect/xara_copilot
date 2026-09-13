from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0.xar')
print(f"Total records: {len(doc.records)}")

# Find all Page definition records
# In Xara, Page tags are Tag 2000, 2001, 2002, 2003, etc., or Chapter/Spread
pages = []
for i, r in enumerate(doc.records):
    # Search for page markers
    if r['tag'] == 2000 or r['tag'] == 2001 or r['tag'] == 2002:
        pages.append((i, r['tag'], r['size']))

print(f"Page tags found: {len(pages)}")
for p in pages:
    print(" ", p)

# Let's search for "Page X of Y" or "X dari Y"
print("\n--- ALL PAGE NUMBER NODES ---")
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        try:
            txt = r['payload'].decode('utf-16le').rstrip('\x00')
            if any(w in txt.lower() for w in ['of 7', 'dari 7', 'of 4', 'dari 4', 'of 3', 'dari 3', 'of 5', 'dari 5']):
                print(f"Rec {i:5d} (Tag {r['tag']}): '{txt}'")
        except:
            pass
