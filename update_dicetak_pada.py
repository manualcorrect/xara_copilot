from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

# Record 1023: CHAR '0' -> '3'
print("Before: record 1023 =", doc.records[1023]["payload"].decode("utf-16le"))
doc.records[1023]["payload"] = "3".encode("utf-16le")

# Record 1027: CHAR '2' -> '1'
print("Before: record 1027 =", doc.records[1027]["payload"].decode("utf-16le"))
doc.records[1027]["payload"] = "1".encode("utf-16le")

# Record 1035: STR 'Des 2025' -> 'Aug 2026'
print("Before: record 1035 =", doc.records[1035]["payload"].decode("utf-16le"))
doc.records[1035]["payload"] = "Aug 2026".encode("utf-16le")
doc.records[1035]["size"] = len(doc.records[1035]["payload"])

# Save to TEST_REK_ANTIGRAVITY.xar
out_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
doc.save(out_path)

# Verify reloaded
doc_verify = XarDocument(out_path)
print("\nAfter update verification:")
print("  Rec 1023:", doc_verify.records[1023]["payload"].decode("utf-16le"))
print("  Rec 1027:", doc_verify.records[1027]["payload"].decode("utf-16le"))
print("  Rec 1035:", doc_verify.records[1035]["payload"].decode("utf-16le"))

c1 = doc_verify.records[1023]["payload"].decode("utf-16le")
c2 = doc_verify.records[1027]["payload"].decode("utf-16le")
st = doc_verify.records[1035]["payload"].decode("utf-16le")
print(f"  Combined 'Dicetak pada' date: '{c1}{c2} {st}'")
