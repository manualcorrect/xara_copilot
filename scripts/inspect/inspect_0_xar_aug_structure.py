from xar_dom_engine import XarDocument
import struct

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\aug\0.xar'
doc = XarDocument(xar_path)
print(f"Total records in 0.xar: {len(doc.records):,}")

# 1. Map all rows (Tag 2204)
rows_map = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2204 and i > 1500:
        saldo_rec = None
        for k in range(i+1, min(len(doc.records), i+8)):
            if doc.records[k]['tag'] in (2201, 2202):
                txt = doc.records[k]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0') and ('.' in txt or len(txt) > 5):
                    saldo_rec = k
                    break
        if saldo_rec:
            row_no_rec = None
            row_no_val = None
            for p in range(max(0, i-6), i):
                if doc.records[p]['tag'] in (2201, 2202):
                    r_txt = doc.records[p]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                    if r_txt.isdigit():
                        row_no_rec = p
                        row_no_val = int(r_txt)
                        break
            if row_no_rec:
                rows_map.append({
                    'row_no_val': row_no_val,
                    'row_no_rec': row_no_rec,
                    'saldo_rec': saldo_rec,
                    'saldo_val': doc.records[saldo_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00'),
                    'tag2204_rec': i
                })

print(f"\n[*] Total Rows mapped in 0.xar: {len(rows_map)}")
print(f"  First 5 rows: {rows_map[:5]}")
print(f"  Last 5 rows: {rows_map[-5:]}")

# 2. Page numbers and total pages
page_headers = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'dari' in txt:
            page_headers.append((i, txt))
print(f"\n[*] Page headers found ({len(page_headers)}): {page_headers}")

# 3. Name stories
name_stories = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if any(w in txt for w in ['ROY', 'DARWIN', 'MASRIYAH', 'ANWAR', 'DINI']):
            name_stories.append((i, txt))
print(f"\n[*] Name stories found ({len(name_stories)}): {name_stories}")

# 4. Period headers
period_headers = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'Jul 2026' in txt or 'Aug 2026' in txt or 'Jun 2026' in txt:
            if '-' in txt or '01' in txt or '31' in txt:
                period_headers.append((i, txt))
print(f"\n[*] Period headers found ({len(period_headers)}): {period_headers}")

# 5. Financial summary in Header Page 1
print("\n=== FINANCIAL SUMMARY IN 0.xar (AROUND RECORD 1000-1400) ===")
for i in range(1100, 1350):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if any(c in txt for c in [',00', ',81', '+', '-', 'Saldo', 'Dana']):
            print(f"  Rec [{i}] Tag {r['tag']}: {txt!r}")
