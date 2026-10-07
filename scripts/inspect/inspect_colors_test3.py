from xar_dom_engine import XarDocument

target_file = r'C:\Users\Lenovo\Downloads\rekening\Antigravity\test\Test_2\test_3.1_tahap6.xar'
doc = XarDocument(target_file)

# Let's inspect Tag 150 for Row 1 (+15.000,00), Row 2 (-16.000,00), and Saldo
# In check_row_diffs, we have found_pairs
from compare_test3_with_user_table import found_pairs

# Check Row 1:
# Pair 1: Saldo (found_pairs[1]), Nominal (found_pairs[2])
s1 = found_pairs[1]
n1 = found_pairs[2]
s2 = found_pairs[3]
n2 = found_pairs[4]

def get_color(story_start, first_text_rec):
    for j in range(story_start, first_text_rec):
        if doc.records[j]['tag'] == 150:
            return j, doc.records[j]['payload'].hex()
    return None

print(f"Row 1 Saldo (41.683,00) Color: {get_color(s1[1], s1[4][0][0])}")
print(f"Row 1 Nominal (+15.000,00) Color: {get_color(n1[1], n1[4][0][0])}")
print(f"Row 2 Saldo (25.683,00) Color: {get_color(s2[1], s2[4][0][0])}")
print(f"Row 2 Nominal (-16.000,00) Color: {get_color(n2[1], n2[4][0][0])}")

# Let's check header summary colors:
# Dana Masuk (1275):
dm_color = [doc.records[j]['payload'].hex() for j in range(1268, 1275) if doc.records[j]['tag'] == 150]
# Dana Keluar (1292):
dk_color = [doc.records[j]['payload'].hex() for j in range(1283, 1292) if doc.records[j]['tag'] == 150]
# Saldo Akhir (1304):
sa_color = [doc.records[j]['payload'].hex() for j in range(1294, 1304) if doc.records[j]['tag'] == 150]

print(f"Header Dana Masuk Color: {dm_color}")
print(f"Header Dana Keluar Color: {dk_color}")
print(f"Header Saldo Akhir Color: {sa_color}")
