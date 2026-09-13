from xar_dom_engine import XarDocument

doc3 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

print("=== doc3 (test_3.1) font 13 records ===")
first_idx = None
last_idx = None
chars3 = []
for i, r in enumerate(doc3.records):
    if r['tag'] in (2000, 4350, 4351):
        fid = int.from_bytes(r['payload'][:4], 'little')
        if fid == 13:
            if first_idx is None: first_idx = i
            last_idx = i
            if r['tag'] == 4350:
                char_code = int.from_bytes(r['payload'][4:6], 'little')
                ch = chr(char_code) if 32 <= char_code <= 126 else f'0x{char_code:04x}'
                chars3.append((i, ch, len(r['payload'])))
            elif r['tag'] == 4351:
                chars3.append((i, "KERNING", len(r['payload'])))
            elif r['tag'] == 2000:
                chars3.append((i, "TAG2000", len(r['payload'])))

print(f"Total Font 13 records in doc3: {len(chars3)}, range: {first_idx}..{last_idx}")
for item in chars3:
    if item[1] in '0123456789' or item[1] in ("KERNING", "TAG2000"):
        print(f"  Index {item[0]}: {item[1]} (len={item[2]})")

print("\n=== doc7 (test_v2.1_tahap7) font 13 records ===")
first_idx7 = None
last_idx7 = None
chars7 = []
for i, r in enumerate(doc7.records):
    if r['tag'] in (2000, 4350, 4351):
        fid = int.from_bytes(r['payload'][:4], 'little')
        if fid == 13:
            if first_idx7 is None: first_idx7 = i
            last_idx7 = i
            if r['tag'] == 4350:
                char_code = int.from_bytes(r['payload'][4:6], 'little')
                ch = chr(char_code) if 32 <= char_code <= 126 else f'0x{char_code:04x}'
                chars7.append((i, ch, len(r['payload'])))
            elif r['tag'] == 4351:
                chars7.append((i, "KERNING", len(r['payload'])))
            elif r['tag'] == 2000:
                chars7.append((i, "TAG2000", len(r['payload'])))

print(f"Total Font 13 records in doc7: {len(chars7)}, range: {first_idx7}..{last_idx7}")
for item in chars7:
    if item[1] in '0123456789' or item[1] in ("KERNING", "TAG2000"):
        print(f"  Index {item[0]}: {item[1]} (len={item[2]})")
