from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# Let's inspect each row by looking at each block of text between header/footer elements
# In Xara, each transaction row is a group containing:
# - Date & Time
# - Description
# - Saldo
# - Nominal
# Let's find all Saldo and Nominal text records across the entire document
# Saldo and Nominal always have Tag 2201 and contain digits and ',' or '.' or '+' or '-'

rows = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        s = r['payload'].decode('utf-16le', errors='replace')
        # Check if it starts with '+' or '-' or is a saldo with ',00' / ',0'
        if (s.startswith('+') or s.startswith('-')) and any(c.isdigit() for c in s):
            # This is a Nominal!
            # Find associated color
            color_rec = None
            color_hex = None
            for j in range(max(0, i-20), i):
                if doc.records[j]['tag'] == 150:
                    color_rec = j
                    color_hex = doc.records[j]['payload'].hex()
            # Find Tag 2206 width
            width_rec = None
            width_val = None
            for j in range(max(0, i-10), i):
                if doc.records[j]['tag'] == 2206 and len(doc.records[j]['payload']) == 12:
                    import struct
                    w = struct.unpack('<iii', doc.records[j]['payload'])
                    width_rec = j
                    width_val = w[0]
            # Find Tag 2100 matrix
            matrix_rec = None
            matrix_x = None
            for j in range(max(0, i-25), i):
                if doc.records[j]['tag'] == 2100 and len(doc.records[j]['payload']) == 12:
                    import struct
                    # Tag 2100 payload has 3 int32: [unk, x, y] or similar
                    m = struct.unpack('<iii', doc.records[j]['payload'])
                    matrix_rec = j
                    matrix_x = m[1]
            
            # Check next record for split
            splits = []
            for k in range(i+1, min(len(doc.records), i+10)):
                rk = doc.records[k]
                if rk['tag'] in (2201, 2202):
                    sk = rk['payload'].decode('utf-16le', errors='replace')
                    if any(c.isdigit() for c in sk) or sk in (',00', '00', '0', '0,00', '0,0'):
                        splits.append((k, rk['tag'], sk))
                elif rk['tag'] == 2203: # end of story
                    break
            
            rows.append({
                'type': 'NOMINAL',
                'rec': i,
                'text': s,
                'color_rec': color_rec,
                'color_hex': color_hex,
                'width_rec': width_rec,
                'width_val': width_val,
                'matrix_rec': matrix_rec,
                'matrix_x': matrix_x,
                'splits': splits
            })
        elif (',00' in s or ',0' in s or ',') and any(c.isdigit() for c in s) and not any(w in s for w in ['Dec', 'Jan', 'Apr', 'Kav', '12190', 'Saldo', 'Dana', 'Awal', 'Akhir', '163000']):
            # This is likely a Saldo (or summary)!
            # Let's filter out summary records (1266, 1275, 1292, 1304)
            if i not in (1266, 1275, 1292, 1304):
                color_rec = None
                color_hex = None
                for j in range(max(0, i-20), i):
                    if doc.records[j]['tag'] == 150:
                        color_rec = j
                        color_hex = doc.records[j]['payload'].hex()
                width_rec = None
                width_val = None
                for j in range(max(0, i-10), i):
                    if doc.records[j]['tag'] == 2206 and len(doc.records[j]['payload']) == 12:
                        import struct
                        w = struct.unpack('<iii', doc.records[j]['payload'])
                        width_rec = j
                        width_val = w[0]
                matrix_rec = None
                matrix_x = None
                for j in range(max(0, i-25), i):
                    if doc.records[j]['tag'] == 2100 and len(doc.records[j]['payload']) == 12:
                        import struct
                        m = struct.unpack('<iii', doc.records[j]['payload'])
                        matrix_rec = j
                        matrix_x = m[1]
                splits = []
                for k in range(i+1, min(len(doc.records), i+10)):
                    rk = doc.records[k]
                    if rk['tag'] in (2201, 2202):
                        sk = rk['payload'].decode('utf-16le', errors='replace')
                        if any(c.isdigit() for c in sk) or sk in (',00', '00', '0', '0,00', '0,0'):
                            splits.append((k, rk['tag'], sk))
                    elif rk['tag'] == 2203:
                        break
                rows.append({
                    'type': 'SALDO',
                    'rec': i,
                    'text': s,
                    'color_rec': color_rec,
                    'color_hex': color_hex,
                    'width_rec': width_rec,
                    'width_val': width_val,
                    'matrix_rec': matrix_rec,
                    'matrix_x': matrix_x,
                    'splits': splits
                })

print(f"Total extracted numeric records: {len(rows)}")
nominals = [r for r in rows if r['type'] == 'NOMINAL']
saldos = [r for r in rows if r['type'] == 'SALDO']
print(f"Nominals found: {len(nominals)}")
print(f"Saldos found: {len(saldos)}")
