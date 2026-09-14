import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar')
print(f"Total records in 0_tahap7.xar: {len(doc.records):,}")

print("\n=== COMPREHENSIVE VERIFICATION OF ALL 8 PAGES ===")

# 1. Name Stories
for p in range(1, 9):
    print(f"\n--- PAGE {p} NAME STORY ---")
    found = False
    for i, r in enumerate(doc.records):
        if r['tag'] == 2201 and 'MASRIYAH' in r['payload'].decode('utf-16le', errors='ignore'):
            # find story start (Tag 2100) and end (Tag 2203)
            start = i
            for k in range(i, max(0, i-30), -1):
                if doc.records[k]['tag'] == 2100:
                    start = k
                    break
            end = i
            for k in range(i, min(len(doc.records), i+30)):
                if doc.records[k]['tag'] == 2203:
                    end = k + 1
                    while end < len(doc.records) and doc.records[end]['tag'] == 0:
                        end += 1
                    break
            
            # Print summary of this story
            c = struct.unpack('<iii', doc.records[start]['payload'])
            w = struct.unpack('<iB', doc.records[start+2]['payload'])[0]
            p1 = struct.unpack('<i', doc.records[start+14]['payload'])[0]
            p2 = struct.unpack('<i', doc.records[start+15]['payload'])[0]
            sz = struct.unpack('<i', doc.records[start+16]['payload'])[0]
            t1 = doc.records[start+20]['payload'].decode('utf-16le', errors='ignore')
            t2 = doc.records[start+26]['payload'].decode('utf-16le', errors='ignore')
            k1 = struct.unpack('<iii', doc.records[start+19]['payload'])
            k2 = struct.unpack('<iii', doc.records[start+25]['payload'])

            print(f"  Record range: [{start}..{end}]")
            print(f"  Coords: X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm")
            print(f"  Width (Tag 2150): {w} mp ({w/28346.4567:.3f}cm)")
            print(f"  Font Size (Tag 2901): {sz} mp ({sz/1000:.1f}pt)")
            print(f"  Line Pitch (Tag 4208/4209): {p1} / {p2} ({p1/500*100:.1f}%)")
            print(f"  Line 1: {t1!r} (kern/lead={k1})")
            print(f"  Line 2: {t2!r} (kern/lead={k2})")
            found = True
            break

# 2. Cabang Objects
print("\n--- ALL CABANG OBJECTS ---")
cabang_count = 0
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and 'KCP Jakarta Taman Aries' in r['payload'].decode('utf-16le', errors='ignore'):
        cabang_count += 1
        # find preceding Tag 2100
        for k in range(i, max(0, i-25), -1):
            if doc.records[k]['tag'] == 2100:
                c = struct.unpack('<iii', doc.records[k]['payload'])
                print(f"  Cabang {cabang_count} at Rec [{i}]: Coords=(X={c[0]/28346.4567:.3f}cm, Y={c[1]/28346.4567:.3f}cm)")
                break

# 3. Period Dates
print("\n--- ALL PERIOD DATES ---")
p_count = 0
for i, r in enumerate(doc.records):
    if r['tag'] == 2201 and '01 Jul 2026 - 31 Jul 2026' in r['payload'].decode('utf-16le', errors='ignore'):
        p_count += 1
        print(f"  Period Date {p_count} at Rec [{i}]: {r['payload'].decode('utf-16le', errors='ignore')!r}")
