import struct
from xar_dom_engine import XarDocument

def clean_period_spaces():
    target_xar = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0_tahap7.xar'
    doc = XarDocument(target_xar)
    print(f"[*] Loaded document: {len(doc.records):,} records")

    # Find all occurrences of Tag 2201 with '01 Jul 2026 - 31 Jul 2026'
    # Check if there is an orphan Tag 2202 or phantom empty node before Tag 4200 / Tag 2201
    
    # We will scan backwards from the end so index removals don't shift upcoming targets
    period_indices = []
    for i, r in enumerate(doc.records):
        if r['tag'] == 2201:
            txt = r['payload'].decode('utf-16le', errors='ignore')
            if '01 Jul 2026 - 31 Jul 2026' in txt:
                period_indices.append(i)

    print(f"[*] Found {len(period_indices)} Period Date stories: {period_indices}")

    for p_idx in reversed(period_indices):
        # Look backwards from p_idx for Tag 2202 and any associated tags between Tag 4410 and Tag 4200
        # Specifically: Tag 4410 -> Tag 1 -> Tag 4405 -> Tag 0 -> Tag 2202 -> Tag 1 -> Tag 4405 -> Tag 0 -> Tag 4200 ...
        # Let's inspect the 15 records preceding p_idx
        start_check = max(0, p_idx - 15)
        del_start = None
        del_end = None
        for k in range(p_idx - 1, start_check, -1):
            if doc.records[k]['tag'] == 2202:
                # The phantom block around Tag 2202 is:
                # [Tag 1, Tag 4405, Tag 0, Tag 2202, Tag 1, Tag 4405, Tag 0]
                # Let's find exact bounds
                # If preceding node is Tag 0 (from Tag 4405) or Tag 4410
                t2202_idx = k
                # If Tag 2202 is followed by Tag 1, Tag 4405, Tag 0
                fwd = t2202_idx + 1
                if fwd < p_idx and doc.records[fwd]['tag'] == 1:
                    # del up to the Tag 0 after Tag 4405
                    while fwd < p_idx and doc.records[fwd]['tag'] in (1, 4405, 0):
                        fwd += 1
                
                # Check backwards for Tag 1, Tag 4405, Tag 0 before Tag 2202
                bwd = t2202_idx
                if doc.records[bwd - 1]['tag'] == 0 and doc.records[bwd - 2]['tag'] == 4405 and doc.records[bwd - 3]['tag'] == 1:
                    bwd = bwd - 3

                del_start = bwd
                del_end = fwd
                break

        if del_start is not None and del_end is not None:
            del_tags = [doc.records[x]['tag'] for x in range(del_start, del_end)]
            print(f"[*] Removing phantom Tag 2202 block at [{del_start}..{del_end}]: tags={del_tags}")
            del doc.records[del_start:del_end]

    for r in doc.records:
        r['size'] = len(r['payload'])

    doc.save(target_xar)
    print(f"[SUCCESS] Cleaned all Period spaces across document! Total records: {len(doc.records):,}")

if __name__ == '__main__':
    clean_period_spaces()
