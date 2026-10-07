from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

curr_story = None
with open('all_texts_utf8.txt', 'w', encoding='utf-8') as out:
    for i, r in enumerate(doc.records):
        if r['tag'] == 2000:
            curr_story = i
        if r['tag'] in (2201, 2202):
            try:
                txt = r['payload'].decode('utf-16le').rstrip('\x00')
                if len(txt.strip()) > 0:
                    out.write(f"Rec {i:4d} | Story {curr_story} | Tag {r['tag']} | Len {len(r['payload'])}: {repr(txt)}\n")
            except:
                pass
print("Done writing all_texts_utf8.txt")
