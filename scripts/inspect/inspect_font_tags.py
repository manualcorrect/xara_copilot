from xar_dom_engine import XarDocument
import struct

doc3 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

def inspect_font_ref(doc, search_text, doc_name):
    print(f"\n=== Searching '{search_text}' in {doc_name} ===")
    for i, r in enumerate(doc.records):
        if r['tag'] in [2201, 2202]:
            txt = r['payload'].decode('utf-16le', errors='replace').strip('\x00')
            if search_text in txt:
                print(f"Found text record [{i}] Tag={r['tag']} : '{txt}'")
                # Look backwards for font attribute tags (Tag 2207, Tag 2901, Tag 2000, Tag 176, Tag 177, etc.)
                for k in range(max(0, i-40), i+1):
                    rec = doc.records[k]
                    tag = rec['tag']
                    p = rec['payload']
                    desc = ""
                    if tag == 2100:
                        desc = "MATRIX"
                    elif tag == 2206:
                        desc = "TAG_TEXT_LINE"
                    elif tag in [2207, 2208, 2209, 2210]:
                        desc = f"FONT_ATTR? payload={p.hex()}"
                    elif tag in [176, 177, 178]:
                        desc = f"FONT_FACE? payload={p.hex()}"
                    elif tag in [2901, 2902, 2904, 2906, 2907, 2908, 2911, 2913, 2918, 2919]:
                        desc = f"FONT_DEF? Tag={tag} payload={p[:30]}"
                    elif tag == 150:
                        desc = f"COLOR hex={p.hex()}"
                    elif tag in [2201, 2202]:
                        desc = f"TEXT '{p.decode('utf-16le', errors='replace').strip(chr(0))}'"
                    if desc:
                        print(f"  [{k:5d}] Tag={tag:4d} (0x{tag:04X}) Size={len(p):3d} : {desc}")
                break

inspect_font_ref(doc3, "95.183,00", "test_3.1.xar")
inspect_font_ref(doc7, "1.619.955,00", "test_v2.1_tahap7.xar")
