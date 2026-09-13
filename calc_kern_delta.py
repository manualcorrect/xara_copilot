from dump_saldo_samples import data

# Let's inspect equations
# dx(row_num, saldo_str)
# Each row has a row number (e.g. '1', '2', ..., '73') and saldo string (e.g. '395.950,81')
# Let's see: row_no also has width!
# Total width = width(row_no) + kern_dx + width(saldo_str) = Constant!
# Therefore: kern_dx = Constant - width(row_no) - width(saldo_str)!

print("=" * 80)
print("TESTING KERN FORMULA: dx = CONST - width(row_no) - width(saldo_str)")
print("=" * 80)

# Let's check rows with 2-digit row numbers (e.g. 10 to 73):
# Row 10: '10', '2.181.835,81' -> dx=62330
# Row 11: '11', '2.179.335,81' -> dx=62545
# Row 12: '12', '279.335,81'   -> dx=62940
# Row 13: '13', '278.335,81'   -> dx=62925
# Row 14: '14', '229.335,81'   -> dx=62895

# Notice:
# In 2-digit rows:
# '279.335,81' (dx=62940) vs '2.181.835,81' (dx=62330) -> delta = 610!
# '278.335,81' (dx=62925) vs '279.335,81' (dx=62940) -> delta = 15!
# '229.335,81' (dx=62895) vs '279.335,81' (dx=62940) -> delta = 45!

# Let's test standard digit widths:
# 0: 512, 1: 340, 2: 512, 3: 512, 4: 512, 5: 512, 6: 512, 7: 512, 8: 512, 9: 512, '.': 256, ',': 256
# Let's check if '2.' = width('2') + width('.') = ~512 + ~256 = ~768 (or ~610 in dx)!

# For a given target saldo string S in rows 56..73:
# Row 56: '56', new_saldo = '6.502.335,81'
# In 0.xar: Row 56 had '56', old_saldo = '146.335,81', dx=62810
# '146.335,81' has 10 chars.
# '6.502.335,81' has 12 chars (adds '6.').
# '6.' delta in dx is approximately -610!
# So for '6.502.335,81': dx = 62810 - 610 = 62200!
# dy = round(dx * 72) = round(62200 * 72) = 4478400!
print("Calculated delta for '6.' in dx is approx -610, bringing dx to ~62200 and dy to ~4478400")
