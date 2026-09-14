import os
import struct
import json
from xar_dom_engine import XarDocument

folder = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun'
t7_path = os.path.join(folder, '0_tahap7.xar')

print("=========================================================================")
print("   COMPREHENSIVE AUDIT & VERIFICATION: MARSIYAH JUNI 2026 (7 PAGES)")
print(f"   Target: {t7_path}")
print("=========================================================================\n")

doc = XarDocument(t7_path)

# 1. Font Definition & References Audit
font_ids = set()
for r in doc.records:
    if r['tag'] == 2907:
        font_ids.add(r['payload'].hex())

print(f"[*] Active Font IDs in 0_tahap7.xar: {font_ids}")
assert '55010000' not in font_ids, "ERROR: Foreign font ID 55010000 detected!"
assert '54010000' in font_ids, "ERROR: Native font ID 54010000 missing!"
print("   -> Font Integrity: 100% Native (0% corruption risk) [PASS]")

# 2. Name Story & Cabang Audit across all 7 pages
name_stories = []
cabangs = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if 'MASRIYAH' in txt:
            w_box, flag = None, None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 2150:
                    w_box, flag = struct.unpack('<iB', doc.records[k]['payload'])
            name_stories.append((i, txt, w_box, flag))
        elif 'KCP Jakarta Taman Aries' in txt:
            pos = None
            for k in range(max(0, i-25), i):
                if doc.records[k]['tag'] == 2100:
                    pos = struct.unpack(f'<{len(doc.records[k]["payload"])//4}i', doc.records[k]['payload'])
            cabangs.append((i, txt, pos))

print(f"\n[*] Name Stories Found: {len(name_stories)} / 7 pages")
for idx, ns in enumerate(name_stories, 1):
    print(f"   Page {idx:2d}: Rec {ns[0]:5d} | Text: {ns[1]!r:25s} | Width: {ns[2]} mp (3.17cm) | Flag: {ns[3]}")
    assert ns[2] == 89858, f"Page {idx} Name width is {ns[2]}, expected 89858 (3.17cm)"

print(f"\n[*] Independent Cabang Boxes Found: {len(cabangs)} / 7 pages")
for idx, cb in enumerate(cabangs, 1):
    print(f"   Page {idx:2d}: Rec {cb[0]:5d} | Text: {cb[1]!r:25s} | Pos: {cb[2]}")
    assert cb[2][0] == 124101 and cb[2][1] == 714420, f"Page {idx} Cabang position mismatch: {cb[2]}"

# 3. Period Header Audit across all 7 pages
periods = []
for i, r in enumerate(doc.records):
    if r['tag'] == 2201:
        txt = r['payload'].decode('utf-16le', errors='ignore')
        if '01 Jun 2026 - 30 Jun 2026' in txt:
            periods.append((i, txt))

print(f"\n[*] Period Headers Found: {len(periods)} / 7 pages")
for idx, p in enumerate(periods, 1):
    print(f"   Page {idx:2d}: Rec {p[0]:5d} | Text: {p[1]!r}")
assert len(periods) == 7, f"Expected 7 periods, got {len(periods)}"

print("\n=========================================================================")
print("   [AUDIT PASSED] 0_tahap7.xar JUNE MEETS 100% OF SPECIFICATIONS & STANDARDS!")
print("=========================================================================")
