import os, struct
from xar_dom_engine import XarDocument

folder = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUL"
doc_orig = XarDocument(os.path.join(folder, "0.xar"))

print("=== INSPECTING NAME STORY ACROSS ALL PAGES IN 0.xar ===")
for idx, r in enumerate(doc_orig.records):
    if r['tag'] == 2201:
        t = r['payload'].decode('utf-16le', errors='ignore')
        if 'ROY DARWIN' in t and idx not in (13278,):
            print(f"\nPage Header Name at index [{idx:5d}]: '{t}'")
            # check the whole story from preceding Tag 2100 to following Tag 2203
            p_2100 = None
            for k in range(idx, max(0, idx-25), -1):
                if doc_orig.records[k]['tag'] == 2100:
                    p_2100 = k
                    break
            p_2203 = None
            for k in range(idx, min(len(doc_orig.records), idx+25)):
                if doc_orig.records[k]['tag'] == 2203:
                    p_2203 = k
                    break
            print(f"   Story range: [{p_2100} .. {p_2203}]")
            for j in range(p_2100, p_2203 + 2):
                rj = doc_orig.records[j]
                txt = ""
                if rj['tag'] in (2201, 2202):
                    txt = " : '" + rj['payload'].decode('utf-16le', errors='ignore') + "'"
                print(f"      [{j:5d}] Tag {rj['tag']:4d} len={len(rj['payload']):2d} hex={rj['payload'][:20].hex()}{txt}")
