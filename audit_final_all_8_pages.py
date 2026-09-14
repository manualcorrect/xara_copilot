from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar')
print(f"Total records in 0_tahap7.xar: {len(doc.records):,}")

print("\n=== VERIFYING ALL 8 PAGES ===")

# Check Name stories
name_stories = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'MASRIYAH' in r['payload'].decode('utf-16le', errors='ignore'):
        # Check Tag 2100 & 2150 & font & line pitch
        w, fl = struct.unpack('<iB', doc.records[i - 17]['payload']) if doc.records[i - 17]['tag'] == 2150 else (0, 0)
        c = struct.unpack(f'<{len(doc.records[i - 19]["payload"])//4}i', doc.records[i - 19]['payload']) if doc.records[i - 19]['tag'] == 2100 else ()
        sz = struct.unpack('<i', doc.records[i - 3]['payload'])[0] if doc.records[i - 3]['tag'] == 2901 else 0
        p1 = struct.unpack('<i', doc.records[i - 5]['payload'])[0] if doc.records[i - 5]['tag'] == 4208 else 0
        p2 = struct.unpack('<i', doc.records[i - 4]['payload'])[0] if doc.records[i - 4]['tag'] == 4209 else 0
        line1 = doc.records[i]['payload'].decode('utf-16le', errors='ignore')
        line2 = doc.records[i + 5]['payload'].decode('utf-16le', errors='ignore') if i+5 < len(doc.records) and doc.records[i+5]['tag'] == 2201 else ""
        name_stories.append({
            'rec': i,
            'coords': c,
            'width_cm': w / 28346.4567,
            'font_pt': sz / 1000,
            'line_pitch_pct': p1 / 500 * 100,
            'line1': line1,
            'line2': line2
        })

print(f"Found {len(name_stories)} Name stories:")
for idx, ns in enumerate(name_stories, 1):
    print(f"  Page {idx}: Rec [{ns['rec']}] | W={ns['width_cm']:.2f}cm | Font={ns['font_pt']}pt | Pitch={ns['line_pitch_pct']}% | Line1={ns['line1']!r} | Line2={ns['line2']!r}")

# Check Cabang objects
cabang_objs = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'KCP Jakarta Taman Aries' in r['payload'].decode('utf-16le', errors='ignore'):
        # find preceding Tag 2100
        for k in range(i, max(0, i-25), -1):
            if doc.records[k]['tag'] == 2100:
                c = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]['payload'])
                cabang_objs.append({
                    'rec': i,
                    'coords': c,
                    'coords_cm': (c[0]/28346.4567, c[1]/28346.4567),
                    'text': r['payload'].decode('utf-16le', errors='ignore')
                })
                break

print(f"\nFound {len(cabang_objs)} Cabang objects:")
for idx, co in enumerate(cabang_objs, 1):
    print(f"  Page {idx}: Rec [{co['rec']}] | Coords={co['coords_cm'][0]:.3f}cm, {co['coords_cm'][1]:.3f}cm | Text={co['text']!r}")

# Check Period dates
period_dates = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and '01 Jul 2026 - 31 Jul 2026' in r['payload'].decode('utf-16le', errors='ignore'):
        period_dates.append({
            'rec': i,
            'text': r['payload'].decode('utf-16le', errors='ignore')
        })

print(f"\nFound {len(period_dates)} Period dates:")
for idx, pd in enumerate(period_dates, 1):
    print(f"  Page {idx}: Rec [{pd['rec']}] | Text={pd['text']!r}")
