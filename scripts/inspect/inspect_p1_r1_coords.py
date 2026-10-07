from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

MP_PER_CM = 72000 / 2.54 # 28346.4567

for label, rec_idx in [("Nominal Row 1 (Page 1)", 1565), ("Saldo Row 1 (Page 1)", 1544)]:
    # Find story index and records
    txt = doc.records[rec_idx]['payload'].decode('utf-16le', errors='replace')
    
    # find story header before rec_idx
    story_idx = None
    mat_rec = None
    for j in range(rec_idx, max(0, rec_idx-40), -1):
        if doc.records[j]['tag'] in [2203, 2204]: # simple or complex story
            story_idx = j
            break
            
    # find matrix before story
    if story_idx is not None:
        for k in range(story_idx, max(0, story_idx-25), -1):
            if doc.records[k]['tag'] == 2100:
                mx, my = struct.unpack('<ii', doc.records[k]['payload'][:8])
                mat_rec = (k, mx, my, mx / MP_PER_CM, my / MP_PER_CM)
                break
                
    # find kern
    kern_rec = None
    for k in range(rec_idx, max(0, rec_idx-15), -1):
        if doc.records[k]['tag'] == 2206:
            kx, ky = struct.unpack('<ii', doc.records[k]['payload'][:8])
            kern_rec = (k, kx, ky, kx / MP_PER_CM, ky / MP_PER_CM)
            break
            
    # find line width
    line_w = None
    for k in range(rec_idx, max(0, rec_idx-25), -1):
        if doc.records[k]['tag'] == 2200:
            p = doc.records[k]['payload']
            if len(p) >= 4:
                lw = struct.unpack('<i', p[:4])[0]
                line_w = (lw, lw / MP_PER_CM)
            break
            
    print(f"\n--- {label} (Rec {rec_idx}) ---")
    print(f"  Text       : {repr(txt)}")
    if mat_rec:
        print(f"  Matrix 2100: Rec {mat_rec[0]} -> X = {mat_rec[1]} mp ({mat_rec[3]:.3f} cm), Y = {mat_rec[2]} mp ({mat_rec[4]:.3f} cm)")
    if kern_rec:
        print(f"  Kern 2206  : Rec {kern_rec[0]} -> X = {kern_rec[1]} mp ({kern_rec[3]:.3f} cm), Y = {kern_rec[2]} mp ({kern_rec[4]:.3f} cm)")
    if line_w:
        print(f"  Line Width : {line_w[0]} mp ({line_w[1]:.3f} cm)")
        
    # Calculate right edge (X + width)
    if mat_rec and kern_rec:
        # In Xara, text starts at matrix X (or kern X) and extends to X + width
        print(f"  Calculated Left Edge  : {mat_rec[3]:.3f} cm")
        if line_w:
            print(f"  Calculated Right Edge : {mat_rec[3] + line_w[1]:.3f} cm")
