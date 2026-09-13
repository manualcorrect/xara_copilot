from xar_dom_engine import XarDocument
import struct

doc3 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\test_3.1.xar')
doc7 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Copilot_v2\test_v2.1_tahap7.xar')

# Look at Tag 2000 for FontID 13 in test_3.1.xar vs test_v2.1_tahap7.xar
print("=== Tag 2000 Payload Comparison ===")
p3 = doc3.records[336]['payload']
p7 = doc7.records[325]['payload']

print(f"test_3.1 Tag 2000 (len={len(p3)}):")
# Let's see what is after the font names in Tag 2000
parts3 = p3[4:].split(b'\x00\x00')
print("Parts 3:", [p[:20] for p in parts3])

print(f"test_v2.1 Tag 2000 (len={len(p7)}):")
parts7 = p7[4:].split(b'\x00\x00')
print("Parts 7:", [p[:20] for p in parts7])
