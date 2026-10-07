import os, struct
from xar_dom_engine import XarDocument

folder = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUL"
doc = XarDocument(os.path.join(folder, "0_tahap7.xar"))

print("=== 1. CHECKING NAME & CABANG ACROSS ALL 7 PAGES ===")
name_objs = []
cabang_objs = []
for idx, r in enumerate(doc.records):
    if r['tag'] == 2201:
        t = r['payload'].decode('utf-16le', errors='ignore').strip()
        if t == 'ADHIKARYA PUTRA':
            # find y pos
            for k in range(max(0, idx-20), idx):
                if doc.records[k]['tag'] == 2100:
                    y = struct.unpack('<iii', doc.records[k]['payload'][:12])[1]
                    name_objs.append((idx, t, y))
                    break
        elif t == 'KCP Jakarta Taman Aries':
            for k in range(max(0, idx-20), idx):
                if doc.records[k]['tag'] == 2100:
                    y = struct.unpack('<iii', doc.records[k]['payload'][:12])[1]
                    cabang_objs.append((idx, t, y))
                    break

print(f"Name instances: {len(name_objs)} -> {name_objs}")
print(f"Cabang instances: {len(cabang_objs)} -> {cabang_objs}")

print("\n=== 2. CHECKING PALETTE DEFINITIONS & USAGE ===")
blue_saldo_recs = [idx for idx, r in enumerate(doc.records) if r['tag'] == 51 and r['payload'][:3].hex() == '134bba']
print(f"Blue Saldo Tag 51 at index: {blue_saldo_recs}")
if blue_saldo_recs:
    b_handle = blue_saldo_recs[0] + 116
    b_hex = struct.pack('<I', b_handle).hex()
    print(f"Blue Saldo Handle = {b_handle} (hex: {b_hex})")

# Check Saldo row colors on Page 7 (Rows 71-74)
print("\n=== 3. CHECKING PAGE 7 (ROWS 71-74) ===")
for idx, r in enumerate(doc.records):
    if r['tag'] == 2201:
        t = r['payload'].decode('utf-16le', errors='ignore').strip()
        if t in ('9.372.395,81', '9.272.395,81', '9.271.395,81', '9.138.495,81'):
            for k in range(max(0, idx-5), min(len(doc.records), idx+5)):
                if doc.records[k]['tag'] == 150:
                    print(f"Saldo '{t:15s}' -> Tag 150 at [{k:5d}]: {doc.records[k]['payload'].hex()}")
                    break
