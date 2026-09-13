from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# The user table from image:
user_table = [
    # (row, nom, saldo)
    (1, '+15.000,00', '41.683,00'),
    (2, '-16.000,00', '25.683,00'),
    (3, '+700.000,00', '725.683,00'),
    (4, '-2.500,00', '723.183,00'),
    (5, '-500.000,00', '223.183,00'),
    (6, '-100.000,00', '123.183,00'),
    (7, '-2.000,00', '121.183,00'),
    (8, '-15.000,00', '106.183,00'),
    (9, '-11.000,00', '95.183,00'),
    (10, '-2.500,00', '92.683,00'),
    (11, '-15.000,00', '77.683,00'),
    (12, '-2.000,00', '75.683,00'),
    (13, '-15.000,00', '60.683,00'),
    (14, '+300.000,00', '360.683,00'),
    (15, '-300.000,00', '60.683,00'),
    (16, '-19.000,00', '41.683,00'),
    (17, '+214.000,00', '255.683,00'),
    (18, '-30.000,00', '225.683,00'),
    (19, '-200.000,00', '25.683,00'),
    (20, '+250.000,00', '275.683,00'),
    (21, '-200.000,00', '75.683,00'),
    (22, '-18.100,00', '57.583,00'),
    (23, '-6.800,00', '50.783,00'),
    (24, '-2.000,00', '48.783,00'),
    (25, '-15.000,00', '33.783,00'),
    (26, '-5.700,00', '28.083,00'),
    (27, '+300.000,00', '328.083,00'),
    (28, '-300.000,00', '28.083,00'),
    (29, '+3.235.920,00', '3.264.003,00'),
    (30, '-70.000,00', '3.194.003,00'),
    (31, '-500,00', '3.193.503,00'),
    (32, '-97.000,00', '3.096.503,00'),
    (33, '-500,00', '3.096.003,00'),
    (34, '-15.000,00', '3.081.003,00'),
    (35, '-100.000,00', '2.981.003,00'),
    (36, '+300.000,00', '3.281.003,00'),
    (37, '+1.000,00', '3.282.003,00'),
    (38, '-36.500,00', '3.245.503,00'),
    (39, '-200.000,00', '3.045.503,00'),
    (40, '-100.000,00', '2.945.503,00'),
    (41, '-100.000,00', '2.845.503,00'),
    (42, '-500.000,00', '2.345.503,00'),
    (43, '-3.500,00', '2.342.003,00'),
    (44, '-200.000,00', '2.142.003,00'),
    (45, '-1.000.000,00', '1.142.003,00'),
    (46, '-5.000,00', '1.137.003,00'),
    (47, '-5.000,00', '1.132.003,00')
]

# Let's find every transaction pair (Saldo, Nominal) in order across the file
# In Xara, each row has a Saldo story followed by a Nominal story (or Nominal followed by Saldo).
# Let's inspect all stories that contain Tag 2201 with numbers.

found_pairs = []
# We can search through all records and group text stories (delimited by Tag 2200 ... Tag 2203)
i = 0
while i < len(doc.records):
    r = doc.records[i]
    if r['tag'] == 2200: # Text story start
        # collect all text records in this story
        story_recs = []
        j = i + 1
        while j < len(doc.records) and doc.records[j]['tag'] != 2203:
            if doc.records[j]['tag'] in (2201, 2202):
                story_recs.append((j, doc.records[j]['tag'], doc.records[j]['payload'].decode('utf-16le', errors='replace')))
            j += 1
        # Check story text
        story_text = "".join(sr[2] for sr in story_recs).strip()
        # Is this a nominal or saldo?
        if (story_text.startswith('+') or story_text.startswith('-')) and any(c.isdigit() for c in story_text) and not ('Dec' in story_text or 'e-Statement' in story_text):
            found_pairs.append(('NOMINAL', i, j, story_text, story_recs))
        elif any(c in story_text for c in [',00', ',0', ',']) and any(c.isdigit() for c in story_text) and not any(w in story_text for w in ['Dec', 'Jan', 'Kav', '12190', 'Saldo', 'Dana', '163000', 'e-Statement']):
            # Filter out header summary (before record 1400)
            if i > 1400:
                found_pairs.append(('SALDO', i, j, story_text, story_recs))
        i = j
    else:
        i += 1

print(f"Total stories found: {len(found_pairs)}")
for idx, p in enumerate(found_pairs):
    print(f"{idx+1:2d}. {p[0]:7s} [recs {p[1]}-{p[2]}]: {repr(p[3]):20s} | parts: {[sr[2] for sr in p[4]]}")
