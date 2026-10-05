import json

with open('ananda_jul_texts.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('ananda_texts_utf8.txt', 'w', encoding='utf-8') as out:
    for i, item in enumerate(data):
        out.write(f"[{i:3d}] Rec {item['idx']:4d} (Tag {item['tag']:4d}): {repr(item['text'])}\n")

print(f"Saved {len(data)} nodes to ananda_texts_utf8.txt")
