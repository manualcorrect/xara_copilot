from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap7.xar'
doc = XarDocument(target_file)

sa = doc.records[1266]['payload'].decode('utf-16le', errors='replace').strip()
dm = doc.records[1275]['payload'].decode('utf-16le', errors='replace').strip()
dm_split = doc.records[1280]['payload'].decode('utf-16le', errors='replace')
dk = doc.records[1292]['payload'].decode('utf-16le', errors='replace').strip()
s_akhir = doc.records[1304]['payload'].decode('utf-16le', errors='replace').strip()

print(f"Saldo Awal : {repr(sa)}")
print(f"Dana Masuk : {repr(dm)} (split: {repr(dm_split)})")
print(f"Dana Keluar: {repr(dk)}")
print(f"Saldo Akhir: {repr(s_akhir)}")

assert sa == '26.683,00', f"Saldo awal mismatch: {sa}"
assert dm == '+ 5.315.920,00', f"Dana masuk mismatch: {dm}"
assert dm_split == '', f"Dana masuk split mismatch: {dm_split}"
assert dk == '- 4.210.600,00', f"Dana keluar mismatch: {dk}"
assert s_akhir == '1.132.003,00', f"Saldo akhir mismatch: {s_akhir}"

print("\nHEADER SUMMARY 100% VERIFIED!")
