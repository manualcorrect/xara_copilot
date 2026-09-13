import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from xar_dom_engine import XarDocument
import struct

MP_PER_CM = 72000 / 2.54 # 28346.4567

def analyze_trans1_detailed(name, path):
    doc = XarDocument(path)
    print(f"\n==========================================================================")
    print(f"   DOKUMEN: {name}")
    print(f"==========================================================================")
    
    # We want Row 1 on Page 1 (around Y=492000 mp / 17.35 cm from bottom, or ~12.34 cm from top)
    # Let's inspect stories between Rec 1500 and 1600
    stories = []
    current_story = None
    
    for i in range(1450, 1600):
        if i >= len(doc.records): break
        r = doc.records[i]
        tag = r['tag']
        
        if tag in [2203, 2204]: # Story start/complex
            pass
        elif tag == 2100: # Matrix
            mx, my = struct.unpack('<ii', r['payload'][:8])
            current_story = {'matrix_rec': i, 'mx': mx, 'my': my, 'kerns': [], 'strings': [], 'chars': [], 'widths': []}
            stories.append(current_story)
        elif tag == 2206 and current_story is not None:
            kx, ky = struct.unpack('<ii', r['payload'][:8])
            current_story['kerns'].append((i, kx, ky))
        elif tag == 2201 and current_story is not None:
            txt = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
            current_story['strings'].append((i, txt))
        elif tag == 2202 and current_story is not None:
            txt = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
            current_story['chars'].append((i, txt))
        elif tag == 2200 and current_story is not None:
            if len(r['payload']) >= 4:
                w = struct.unpack('<i', r['payload'][:4])[0]
                current_story['widths'].append((i, w))

    for s in stories:
        full_text = "".join(x[1] for x in s['strings'] + s['chars'])
        if any(num in full_text for num in ['100.000', '554.955', '3.744', '-1.000']):
            mx_cm = s['mx'] / MP_PER_CM
            my_cm = s['my'] / MP_PER_CM
            
            # Kern X
            kx_mp = s['kerns'][0][1] if s['kerns'] else 0
            ky_mp = s['kerns'][0][2] if s['kerns'] else 0
            kx_cm = kx_mp / MP_PER_CM
            ky_cm = ky_mp / MP_PER_CM
            
            # Total X position in Xara ruler
            # If text object is at matrix X and has kerning offset kx:
            total_x_mp = s['mx'] + kx_mp
            total_x_cm = total_x_mp / MP_PER_CM
            
            # Line width / text width
            w_mp = s['widths'][0][1] if s['widths'] else 0
            w_cm = w_mp / MP_PER_CM
            
            # Right edge
            right_x_mp = total_x_mp + w_mp
            right_x_cm = right_x_mp / MP_PER_CM
            
            item_type = "NOMINAL" if any(sym in full_text for sym in ['-', '+']) else "SALDO"
            
            print(f"\n[{item_type}] Transaksi 1:")
            print(f"  * Teks                  : '{full_text}'")
            print(f"  * Matrix Rec [{s['matrix_rec']:4d}]       : X = {s['mx']:7d} mp ({mx_cm:.3f} cm), Y = {s['my']:7d} mp ({my_cm:.3f} cm)")
            if s['kerns']:
                print(f"  * Kern Rec [{s['kerns'][0][0]:4d}]         : X = {kx_mp:7d} mp ({kx_cm:.3f} cm), Y = {ky_mp:7d} mp ({ky_cm:.3f} cm)")
            print(f"  * Posisi Mulai Teks (Left) : X = {total_x_mp:7d} mp ({total_x_cm:.3f} cm)")
            if w_mp > 0:
                print(f"  * Estimasi Lebar Teks (W)  : W = {w_mp:7d} mp ({w_cm:.3f} cm)")
                print(f"  * Posisi Ujung Kanan (Right: X = {right_x_mp:7d} mp ({right_x_cm:.3f} cm)")

analyze_trans1_detailed("test_v2.1_tahap7.xar", r"C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar")
analyze_trans1_detailed("test_3.1.xar", r"C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar")
