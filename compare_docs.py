from xar_dom_engine import XarDocument

doc_normal = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')
doc_bold = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7_bold_test.xar')

print('doc_normal len:', len(doc_normal.records))
print('doc_bold len:', len(doc_bold.records))

diffs = []
idx_norm = 0
idx_bold = 0
while idx_norm < len(doc_normal.records) and idx_bold < len(doc_bold.records):
    rn = doc_normal.records[idx_norm]
    rb = doc_bold.records[idx_bold]
    if rn['tag'] == rb['tag'] and rn['payload'] == rb['payload']:
        idx_norm += 1
        idx_bold += 1
    elif rb['tag'] == 4350 and rb['payload'][:4] == b'\x0d\x00\x00\x00' and rb['payload'][4:6] == b'\x39\x00':
        print(f"Glyph 9 inserted at bold index {idx_bold}")
        idx_bold += 1
    else:
        diffs.append((idx_norm, rn['tag'], len(rn['payload']), idx_bold, rb['tag'], len(rb['payload'])))
        idx_norm += 1
        idx_bold += 1
        if len(diffs) > 20:
            break

print('Total other diffs:', len(diffs))
for d in diffs:
    print(d)
