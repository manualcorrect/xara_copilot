from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

# Map rows 56 to 73
new_saldos = {
    56: (13587, "6.502.335,81"),
    57: (13739, "6.465.335,81"),
    58: (13889, "6.715.335,81"),
    59: (14989, "6.650.347,81"),
    60: (15134, "6.649.347,81"),
    61: (15274, "6.613.347,81"),
    62: (15442, "6.583.347,81"),
    63: (15603, "6.383.347,81"),
    64: (15758, "6.483.347,81"),
    65: (15908, "6.482.347,81"),
    66: (16048, "6.382.347,81"),
    67: (16215, "6.682.347,81"),
    68: (16374, "6.482.347,81"),
    69: (16546, "6.582.347,81"),
    70: (16713, "6.382.347,81"),
    71: (17869, "6.582.347,81"),
    72: (18021, "6.382.347,81"),
    73: (18161, "6.377.347,81")
}

print("=" * 80)
print("TAG 2204 CALIBRATION MAPPING FOR ROWS 56 TO 73")
print("=" * 80)

# Digit width deltas relative to baseline
# In 0.xar, we can find the Tag 2204 node right before each saldo node:
for r_num, (s_rec, s_val) in sorted(new_saldos.items()):
    # find Tag 2204 before s_rec
    t2204_rec = None
    for k in range(s_rec - 15, s_rec):
        if doc0.records[k]['tag'] == 2204:
            t2204_rec = k
            break
    
    orig_dx, orig_dy = struct.unpack('<ii', doc0.records[t2204_rec]['payload'][:8])
    orig_txt = doc0.records[s_rec]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
    
    # Calculate length difference:
    # If orig_txt was ~10 chars (e.g. 146.335,81), new is 12 chars (6.502.335,81) -> delta_len = 2 chars
    # If orig_txt was ~9 chars (e.g. 27.347,81), new is 12 chars -> delta_len = 3 chars
    # Average width per char in dx units is ~305, so '6.' (2 chars) is ~610, 3 chars is ~915
    if len(orig_txt) == 10: # e.g. 146.335,81
        new_dx = orig_dx - 610
    elif len(orig_txt) == 9: # e.g. 27.347,81
        new_dx = orig_dx - 915
    elif len(orig_txt) == 8: # e.g. 1.347,81
        new_dx = orig_dx - 1220
    else:
        new_dx = orig_dx - 610
        
    new_dy = round(new_dx * 72)
    print(f"Row {r_num:2d} | Rec {s_rec:5d} | Orig: '{orig_txt:12s}' (dx={orig_dx:5d}, dy={orig_dy:7d}) --> New: '{s_val:12s}' (dx={new_dx:5d}, dy={new_dy:7d}) | Tag 2204 Rec {t2204_rec}")
