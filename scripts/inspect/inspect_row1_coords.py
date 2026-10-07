import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

def inspect_trans1(name, path):
    doc = XarDocument(path)
    print(f"\n==================== {name} ====================")
    txs = doc.get_transactions()
    t1 = next((t for t in txs if t['row'] == 1), None)
    if not t1:
        print("Row 1 not found!")
        return
        
    nom_s = t1['nom_story']
    bal_s = t1['bal_story']
    
    MP_PER_CM = 72000 / 2.54 # 28346.4567 millipoints per cm
    
    print(f"Row 1 Nominal Text: {repr(t1['nominal'])}")
    if nom_s:
        x_mp = nom_s['x']
        y_mp = nom_s['y']
        x_cm = x_mp / MP_PER_CM
        y_cm = y_mp / MP_PER_CM
        
        # Matrix record (Tag 2100) before story
        mat_rec = None
        for j in range(max(0, nom_s['story_idx']-25), nom_s['story_idx']):
            if doc.records[j]['tag'] == 2100:
                mat_x, mat_y = struct.unpack('<ii', doc.records[j]['payload'][:8])
                mat_rec = (j, mat_x, mat_y, mat_x / MP_PER_CM, mat_y / MP_PER_CM)
                
        # Kerning record (Tag 2206)
        kern_rec = None
        for j in range(nom_s['story_idx'], nom_s['end_story_idx']+1):
            if doc.records[j]['tag'] == 2206:
                kx, ky = struct.unpack('<ii', doc.records[j]['payload'][:8])
                kern_rec = (j, kx, ky, kx / MP_PER_CM, ky / MP_PER_CM)
                
        # Line record (Tag 2200) width
        line_w = None
        if nom_s.get('line_indices'):
            p = doc.records[nom_s['line_indices'][0]]['payload']
            if len(p) >= 4:
                lw_mp = struct.unpack('<i', p[:4])[0]
                line_w = (lw_mp, lw_mp / MP_PER_CM)
                
        print(f"  Nominal Story Index : {nom_s['story_idx']}")
        print(f"  Nominal Position X  : {x_mp} mp ({x_cm:.3f} cm)")
        print(f"  Nominal Position Y  : {y_mp} mp ({y_cm:.3f} cm)")
        if mat_rec:
            print(f"  Matrix (Tag 2100)   : Rec {mat_rec[0]} -> X={mat_rec[1]} mp ({mat_rec[3]:.3f} cm), Y={mat_rec[2]} mp ({mat_rec[4]:.3f} cm)")
        if kern_rec:
            print(f"  Kern (Tag 2206)     : Rec {kern_rec[0]} -> X={kern_rec[1]} mp ({kern_rec[3]:.3f} cm), Y={kern_rec[2]} mp ({kern_rec[4]:.3f} cm)")
        if line_w:
            print(f"  Line Width          : {line_w[0]} mp ({line_w[1]:.3f} cm)")
            
    print(f"\nRow 1 Saldo Text: {repr(t1['balance'])}")
    if bal_s:
        x_mp = bal_s['x']
        y_mp = bal_s['y']
        x_cm = x_mp / MP_PER_CM
        y_cm = y_mp / MP_PER_CM
        
        mat_rec = None
        for j in range(max(0, bal_s['story_idx']-25), bal_s['story_idx']):
            if doc.records[j]['tag'] == 2100:
                mat_x, mat_y = struct.unpack('<ii', doc.records[j]['payload'][:8])
                mat_rec = (j, mat_x, mat_y, mat_x / MP_PER_CM, mat_y / MP_PER_CM)
                
        kern_rec = None
        for j in range(bal_s['story_idx'], bal_s['end_story_idx']+1):
            if doc.records[j]['tag'] == 2206:
                kx, ky = struct.unpack('<ii', doc.records[j]['payload'][:8])
                kern_rec = (j, kx, ky, kx / MP_PER_CM, ky / MP_PER_CM)
                
        line_w = None
        if bal_s.get('line_indices'):
            p = doc.records[bal_s['line_indices'][0]]['payload']
            if len(p) >= 4:
                lw_mp = struct.unpack('<i', p[:4])[0]
                line_w = (lw_mp, lw_mp / MP_PER_CM)
                
        print(f"  Saldo Story Index   : {bal_s['story_idx']}")
        print(f"  Saldo Position X    : {x_mp} mp ({x_cm:.3f} cm)")
        print(f"  Saldo Position Y    : {y_mp} mp ({y_cm:.3f} cm)")
        if mat_rec:
            print(f"  Matrix (Tag 2100)   : Rec {mat_rec[0]} -> X={mat_rec[1]} mp ({mat_rec[3]:.3f} cm), Y={mat_rec[2]} mp ({mat_rec[4]:.3f} cm)")
        if kern_rec:
            print(f"  Kern (Tag 2206)     : Rec {kern_rec[0]} -> X={kern_rec[1]} mp ({kern_rec[3]:.3f} cm), Y={kern_rec[2]} mp ({kern_rec[4]:.3f} cm)")
        if line_w:
            print(f"  Line Width          : {line_w[0]} mp ({line_w[1]:.3f} cm)")

inspect_trans1('test_v2.1_tahap7.xar', r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')
inspect_trans1('test_v2.1_tahap6.xar', r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap6.xar')
inspect_trans1('test_3.1.xar', r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
