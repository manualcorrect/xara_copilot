from xar_dom_engine import XarDocument
from collections import Counter

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)

colors = [r['payload'].hex() for r in doc.records if r['tag'] == 150]
c_counts = Counter(colors)

print("=" * 80)
print("TAG 150 COLOR PALETTE IN JUL 0.XAR")
print("=" * 80)
for hex_col, cnt in c_counts.most_common(20):
    print(f"Color: b'{hex_col}' | Count: {cnt}")
