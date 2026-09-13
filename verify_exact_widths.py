from collect_font_samples import all_samples

# Using our known relations relative to w2:
# w0 = w2 + 676
# w1 = w2 - 1602
# w2 = w2
# w3 = w2 + 78
# w4 = w2 + 277
# w5 = w2 + 78
# w7 = w2 - 360
# w8 = w2 + 200

# Now solve w2, w6, w9, w_dot, w_comma, w_minus, w_plus
# Let's list samples:
candidates = [
    ('25.683,00', 38241),
    ('225.683,00', 43003),
    ('2.345.503,00', 50237),
    ('-2.500,00', 37635),
    ('-500,00', 31033),
    ('-180.080,00', 46555),
    ('-500.000,00', 49187),
    ('-1.000.000,00', 54785),
    ('+5.406.000,00', 56546),
    ('92.683,00', 38279),
    ('95.183,00', 36639),
    ('60.683,00', 38955),
    ('106.183,00', 40397),
]

# Look at:
# '225.683,00' - '25.683,00' = 43003 - 38241 = 4762 mp = w2!
# WOW! Look at that: '225.683,00' vs '25.683,00' differs by exactly one '2'!
# 43003 - 38241 = 4762 millipoints!
# So w2 = 4762 millipoints!
w2 = 4762
w0 = w2 + 676      # 5438
w1 = w2 - 1602     # 3160
w3 = w2 + 78       # 4840
w4 = w2 + 277      # 5039
w5 = w2 + 78       # 4840
w7 = w2 - 360      # 4402
w8 = w2 + 200      # 4962

# Check 92.683 vs 25.683:
# '92.683,00' (38279) - '25.683,00' (38241) = 38 mp -> (w9 + w2) - (w2 + w5) = w9 - w5 = 38 -> w9 = w5 + 38 = 4878!
w9 = w5 + 38 # 4878

# Check 60.683 vs 25.683:
# '60.683,00' (38955) - '25.683,00' (38241) = 714 mp -> (w6 + w0) - (w2 + w5) = 714 -> w6 = 714 + w2 + w5 - w0 = 714 + 4762 + 4840 - 5438 = 4878!
w6 = 714 + w2 + w5 - w0 # 4878

print("Digits:")
print(f"  0: {w0}")
print(f"  1: {w1}")
print(f"  2: {w2}")
print(f"  3: {w3}")
print(f"  4: {w4}")
print(f"  5: {w5}")
print(f"  6: {w6}")
print(f"  7: {w7}")
print(f"  8: {w8}")
print(f"  9: {w9}")

# Now punctuation:
# '25.683,00' = w2 + w5 + w_dot + w6 + w8 + w3 + w_comma + w0 + w0 = 38241
# sum digits = w2 + w5 + w6 + w8 + w3 + 2*w0 = 4762 + 4840 + 4878 + 4962 + 4840 + 2*5438 = 35158
# w_dot + w_comma = 38241 - 35158 = 3083 mp!

# Look at:
# '-2.500,00' (37635) vs '-500,00' (31033) = 6602 mp = w_dot + w2 = 6602 -> w_dot = 6602 - 4762 = 1840 mp!
w_dot = 6602 - w2 # 1840
w_comma = 3083 - w_dot # 1243

# Look at:
# '-500,00' = w_minus + w5 + 3*w0 + w_comma = 31033
# w_minus = 31033 - (w5 + 3*w0 + w_comma) = 31033 - (4840 + 3*5438 + 1243) = 31033 - 22397 = 8636 mp?
# Wait, '-500,00' has two 0s: '-500,00' -> 5, 0, 0, comma, 0, 0 -> four 0s!
# w_minus = 31033 - (4840 + 4*5438 + 1243) = 31033 - 27835 = 3198 mp!
w_minus = 31033 - (w5 + 4*w0 + w_comma)

# Look at '+5.406.000,00' (56546) vs '-1.000.000,00' (54785)
# diff = 56546 - 54785 = 1761
# '+5.406.000,00' - '-1.000.000,00' = (w_plus - w_minus) + (w5 + w4 + w6 - w1)
# 1761 = (w_plus - w_minus) + (4840 + 5039 + 4878 - 3160) = (w_plus - w_minus) + 11597
# wait, '+350.000,00' (49790) vs '-500.000,00' (49187):
# 49790 - 49187 = 603 = (w_plus - w_minus) + (w3 - w0) = (w_plus - w_minus) + (4840 - 5438) = (w_plus - w_minus) - 598
# w_plus - w_minus = 603 + 598 = 1201 mp!
w_plus = w_minus + 1201

print(f"\nPunctuation & Signs:")
print(f"  .: {w_dot}")
print(f"  ,: {w_comma}")
print(f"  -: {w_minus}")
print(f"  +: {w_plus}")

# VERIFY ALL 48 COMPLETE SAMPLES!
glyph_map = {
    '0': w0, '1': w1, '2': w2, '3': w3, '4': w4,
    '5': w5, '6': w6, '7': w7, '8': w8, '9': w9,
    '.': w_dot, ',': w_comma, '-': w_minus, '+': w_plus
}

from collect_font_samples import all_samples
complete_samples = [s for s in all_samples if s[0].endswith(',00') and all(c in glyph_map for c in s[0])]

print(f"\nVerification on {len(complete_samples)} samples:")
max_diff = 0
for txt, w in sorted(complete_samples, key=lambda x: len(x[0])):
    pred = sum(glyph_map[c] for c in txt)
    diff = abs(pred - w)
    if diff > max_diff:
        max_diff = diff
    print(f"  {txt:18s} : actual={w}, pred={pred}, diff={diff}")

print(f"\nMAX DIFFERENCE ACROSS ALL SAMPLES: {max_diff} millipoints ({max_diff/28346.4567:.5f} cm)!")
