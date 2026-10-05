import json
from xar_dom_engine import XarDocument

with open("aug_stories_extracted.json", "r", encoding="utf-8") as f:
    stories = json.load(f)

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar")

# Let's inspect all rows:
# Find all nominal candidates and match them to the 36 rows
# Let's see: In Aug 0.xar, what are the original 36 transactions?
# Let's write an algorithm to discover all 36 rows in order

rows = []
for i, st in enumerate(stories):
    txt = st['text'].strip()
    idx = st['idx']
    # If text is an amount (+..., -..., or digits with comma/period)
    if (txt.startswith('+') or txt.startswith('-')) and (',' in txt or '.' in txt) and ('WIB' not in txt) and ('Sep' not in txt):
        # This is a nominal node!
        rows.append((idx, txt, i))

print(f"Found {len(rows)} nominal candidate nodes:")
for r in rows:
    print(f"Rec {r[0]:5d}: {r[1]}")
