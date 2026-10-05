import os, struct
from xar_dom_engine import XarDocument

folder = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\ADHIKARYA PUTRA\New folder\JUL"
doc = XarDocument(os.path.join(folder, "0.xar"))

def deteksi_palet_dinamis(doc: XarDocument):
    palette = {}
    for idx, r in enumerate(doc.records):
        if r['tag'] == 51 and len(r['payload']) >= 3:
            rgb = r['payload'][:3].hex()
            handle = idx + 116
            h_bytes = bytearray(struct.pack('<I', handle))
            if rgb == '134bba': # Mandiri Blue Saldo
                palette['blue_saldo'] = h_bytes
                print(f"Detected Blue Saldo: Index {idx}, Handle {handle} (hex: {h_bytes.hex()})")
            elif rgb == '06aa6f': # Mandiri Green Credit
                palette['green_credit'] = h_bytes
                print(f"Detected Green Credit: Index {idx}, Handle {handle} (hex: {h_bytes.hex()})")
            elif rgb == '1a1a1a': # Mandiri Black Debit
                palette['black_debit'] = h_bytes
                print(f"Detected Black Debit: Index {idx}, Handle {handle} (hex: {h_bytes.hex()})")
            elif rgb == '615a5a': # Mandiri Gray Sawal
                palette['gray_sawal'] = h_bytes
                print(f"Detected Gray Sawal: Index {idx}, Handle {handle} (hex: {h_bytes.hex()})")
            elif rgb == '000000' and 'normal_text' not in palette and idx > 500: # Normal text
                palette['normal_text'] = h_bytes
                print(f"Detected Normal Text: Index {idx}, Handle {handle} (hex: {h_bytes.hex()})")
    return palette

pal = deteksi_palet_dinamis(doc)
print("\nDetected Palette:", {k: v.hex() for k, v in pal.items()})
