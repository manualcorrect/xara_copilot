import json
from xar_dom_engine import XarDocument

with open('ananda_jul_texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total Text Nodes: {len(data)}")
for i, item in enumerate(data):
    print(f"[{i:3d}] Rec {item['idx']:4d} (Tag {item['tag']:4d}): {repr(item['text'])}")
