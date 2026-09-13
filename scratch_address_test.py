import struct
from xar_dom_engine import XarDocument

src_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\0_output.xar'
test_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Agu\test_address.xar'

doc = XarDocument(src_path)

def update_text(rec_idx, text):
    p = bytearray(text.encode('utf-16le'))
    doc.records[rec_idx]['payload'] = p
    doc.records[rec_idx]['size'] = len(p)

def blank_text(rec_idx):
    doc.records[rec_idx]['payload'] = bytearray(b'\x00\x00')
    doc.records[rec_idx]['size'] = 2

def set_t2206(rec_idx, w, h, dx):
    doc.records[rec_idx]['payload'] = bytearray(struct.pack('<iii', w, h, dx))
    doc.records[rec_idx]['size'] = 12

def set_t2204(rec_idx, dx, dy):
    doc.records[rec_idx]['payload'] = bytearray(struct.pack('<ii', dx, dy))
    doc.records[rec_idx]['size'] = 8

# Target text parts (matching Jun exactly):
line1 = 'Menara Mandiri 1 Jalan Jenderal Sudirman Kav.'
line2 = ' 54-55, Jakarta 12190, Indonesia'
# Tag 2206 in Jun: (277227, 6481, 0)
KERN_W = 277227
KERN_H = 6481

# 1. PAGE 1 (rec 305..435)
set_t2206(307, KERN_W, KERN_H, 0)
update_text(308, line1[0]) # Tag 2202: 'M'
set_t2204(309, 0, 0)
update_text(313, line1[1:]) # Tag 2201: 'enara Mandiri 1 Jalan Jenderal Sudirman Kav.'
set_t2204(314, 1, 0) # matching Jun Tag 2204 (1, 0)
update_text(318, line2) # Tag 2201: ' 54-55, Jakarta 12190, Indonesia'

# Blank all remaining text and zero kerning in P1 story:
p1_text_nodes = [323, 328, 333, 338, 343, 348, 353, 358, 363, 368, 369, 378, 383, 384, 389, 390, 395, 400, 405, 410, 415, 420, 425, 426, 431]
p1_kern_nodes = [319, 324, 329, 334, 339, 344, 349, 354, 359, 364, 374, 379, 396, 401, 406, 411, 416, 421]

for r in p1_text_nodes:
    blank_text(r)
for r in p1_kern_nodes:
    set_t2204(r, 0, 0)

# 2. PAGE 2 (rec 5295..5312)
set_t2206(5297, KERN_W, KERN_H, 0)
update_text(5298, line1)
set_t2204(5299, 1, 0)
update_text(5303, line2)
set_t2204(5304, 0, 0)
blank_text(5308)

# 3. PAGE 3 (rec 8493..8623)
set_t2206(8495, KERN_W, KERN_H, 0)
update_text(8496, line1[0]) # Tag 2202: 'M'
set_t2204(8497, 0, 0)
update_text(8501, line1[1:]) # Tag 2201: 'enara Mandiri 1 Jalan Jenderal Sudirman Kav.'
set_t2204(8502, 1, 0)
update_text(8506, line2) # Tag 2201: ' 54-55, Jakarta 12190, Indonesia'

p3_text_nodes = [8511, 8516, 8521, 8526, 8531, 8536, 8541, 8546, 8551, 8556, 8557, 8566, 8571, 8572, 8577, 8578, 8583, 8588, 8593, 8598, 8603, 8608, 8613, 8614, 8619]
p3_kern_nodes = [8507, 8512, 8517, 8522, 8527, 8532, 8537, 8542, 8547, 8552, 8562, 8567, 8584, 8589, 8594, 8599, 8604, 8609]

for r in p3_text_nodes:
    blank_text(r)
for r in p3_kern_nodes:
    set_t2204(r, 0, 0)

# Sync all record sizes
for r in doc.records:
    r['size'] = len(r['payload'])

assert len(doc.records) == 13664, f"Record count violation: {len(doc.records)}"
doc.save(test_path)
print(f"SUCCESS! Saved test address update to: {test_path}")
