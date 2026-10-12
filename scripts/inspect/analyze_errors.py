import os
import sys
import struct

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from xar_dom_engine import XarDocument

p_ref = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\0.xar'
p_out = r'D:\X_Files\rekening\PT BENDI NASHA NIAGA INDUSTRI\alhadi\Folder Baru\Jul\0_output.xar'

doc_ref = XarDocument(p_ref)
doc_out = XarDocument(p_out)

print("=========================================================================")
print("  ANALISIS MENDALAM: 0.xar (REFERENSI) vs 0_output.xar (HASIL EKSEKUSI)")
print("=========================================================================\n")

# -------------------------------------------------------------------------
print("=== DETAIL RECORDS 3925 s.d. 4015 DI REF (0.xar) ===")
for j in range(3925, 4015):
    rf = doc_ref.records[j]
    txt = rf['payload'].decode('utf-16le', errors='ignore') if rf['tag'] in (2201, 2202) else ''
    if txt or rf['tag'] in (2100, 2200, 2203):
        print(f"  rec {j:4d} tag {rf['tag']:4d} ({rf['size']:2d}b): {repr(txt)}")





# -------------------------------------------------------------------------
# 2. COLOUR DEFINITIONS (TAG 51 & TAG 150)
# -------------------------------------------------------------------------
print("\n=== 2. ANALISIS WARNA (TAG 51 & TAG 150) ===")
# List all Tag 51 in doc_ref
colors_51_ref = []
for idx, r in enumerate(doc_ref.records):
    if r['tag'] == 51:
        colors_51_ref.append((idx, r['payload'].hex()))
print(f"Total Tag 51 (Definisi Warna) di file 0 (REF): {len(colors_51_ref)}")
for idx, hex_data in colors_51_ref[:10]:
    print(f"  rec {idx}: {hex_data}")

# Check what Tag 150 values are used in doc_ref vs doc_out
tag150_ref = set()
for r in doc_ref.records:
    if r['tag'] == 150:
        tag150_ref.add(r['payload'].hex())

tag150_out = set()
for r in doc_out.records:
    if r['tag'] == 150:
        tag150_out.add(r['payload'].hex())

print(f"\nTag 150 unik di file REF: {len(tag150_ref)}")
for h in sorted(tag150_ref):
    print(f"  REF tag 150: {h}")

print(f"\nTag 150 unik di file OUT: {len(tag150_out)}")
for h in sorted(tag150_out):
    status = "VALID (ada di ref)" if h in tag150_ref else "INVALID / ASING (TIDAK ADA DI REF!)"
    print(f"  OUT tag 150: {h} -> {status}")

# -------------------------------------------------------------------------
# 3. NOMOR HALAMAN (PAGE NUMBERS)
# -------------------------------------------------------------------------
print("\n=== 3. ANALISIS NOMOR HALAMAN DI FILE 0 (REF) ===")
spreads = [i for i, r in enumerate(doc_ref.records) if r['tag'] == 46]
for p_idx, sp in enumerate(spreads):
    p_num = p_idx + 1
    next_sp = spreads[p_idx + 1] if p_idx + 1 < len(spreads) else len(doc_ref.records)
    print(f"\n--- Halaman {p_num} (Records {sp} s.d. {next_sp}) ---")
    for j in range(sp, min(sp + 1000, next_sp)):
        r = doc_ref.records[j]
        if r['tag'] == 2100 and r['size'] >= 8:
            x, y = struct.unpack('<ii', r['payload'][:8])
            if y >= 700000 and x >= 500000:
                print(f"  REF Story {j} at x={x}, y={y}:")
                for k in range(j + 1, min(j + 30, next_sp)):
                    if doc_ref.records[k]['tag'] == 2100:
                        break
                    if doc_ref.records[k]['tag'] in (2201, 2202):
                        t = doc_ref.records[k]['payload'].decode('utf-16le', errors='ignore')
                        ro_t = doc_out.records[k]['payload'].decode('utf-16le', errors='ignore')
                        print(f"    rec {k} tag {doc_ref.records[k]['tag']}: REF={repr(t)} | OUT={repr(ro_t)}")

# -------------------------------------------------------------------------
# 4. TANGGAL & JAM TRANSAKSI (DATE & TIME)
# -------------------------------------------------------------------------
print("\n=== 4. ANALISIS FORMAT TANGGAL & JAM TRANSAKSI DI FILE 0 (REF) ===")
# Inspect date/time stories across table rows in doc_ref
# Find all table rows in doc_ref
saldo_stories_ref = []
for i, r in enumerate(doc_ref.records):
    if r['tag'] == 2100 and r['size'] >= 8:
        x, y = struct.unpack('<ii', r['payload'][:8])
        page = sum(1 for sp in spreads if i >= sp) + 1
        is_table_y = (y <= 520000) if page == 1 else (y <= 660000)
        if 470000 <= x <= 575000 and is_table_y and y >= 40000:
            # check text
            t = ''
            for k in range(i+1, min(i+15, len(doc_ref.records))):
                if doc_ref.records[k]['tag'] == 2100: break
                if doc_ref.records[k]['tag'] in (2201, 2202):
                    t += doc_ref.records[k]['payload'].decode('utf-16le', errors='ignore')
            if ',' in t or '.' in t:
                saldo_stories_ref.append({'idx': i, 'page': page, 'x': x, 'y': y, 'text': t})

saldo_stories_ref.sort(key=lambda s: (s['page'], -s['y']))
print(f"Total baris transaksi terdeteksi di REF: {len(saldo_stories_ref)}")

for r_idx in range(len(saldo_stories_ref)):
    s = saldo_stories_ref[r_idx]
    p_num = s['page']
    row_y = s['y']
    # find date/time stories in ref
    row_recs = []
    for i, r in enumerate(doc_ref.records):
        if r['tag'] == 2100 and r['size'] >= 8:
            x, y = struct.unpack('<ii', r['payload'][:8])
            page = sum(1 for sp in spreads if i >= sp) + 1
            if page == p_num and abs(y - row_y) <= 12000 and 50000 <= x <= 95000:
                t_ref = ''
                for k in range(i+1, min(i+15, len(doc_ref.records))):
                    if doc_ref.records[k]['tag'] == 2100: break
                    if doc_ref.records[k]['tag'] in (2201, 2202):
                        t_ref += doc_ref.records[k]['payload'].decode('utf-16le', errors='ignore')
                t_out = ''
                for k in range(i+1, min(i+15, len(doc_out.records))):
                    if doc_out.records[k]['tag'] == 2100: break
                    if doc_out.records[k]['tag'] in (2201, 2202):
                        t_out += doc_out.records[k]['payload'].decode('utf-16le', errors='ignore')
                row_recs.append((x, y, t_ref, t_out))
    
    if r_idx < 5 or (25 <= r_idx <= 30) or r_idx >= 44:
        print(f"  Baris {r_idx+1:02d} (Hal {p_num}, y={row_y}):")
        for x, y, t_ref, t_out in row_recs:
            print(f"    (x={x}, y={y}): REF={repr(t_ref):<20} | OUT={repr(t_out)}")
