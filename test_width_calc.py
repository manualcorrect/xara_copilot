GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

sample = '5.434.083,00'
w_calc = calc_text_width(sample)
print(f"Sample: {sample} -> Calc Width: {w_calc} mp vs Tag 2206: 50435 mp (diff: {w_calc - 50435})")

# Let's test against several existing strings
samples = [
    ('5.434.083,00', 50435),
    ('+5.406.000,00', 56546),
    ('-180.080,00', 46555),
    ('-1.000.000,00', 54785),
    ('-2.500,00', 37635),
    ('4.183.503,00', 48878),
    ('4.181.003,00', 47796),
    ('3.281.003,00', 49320)
]

for s, w_actual in samples:
    w_c = calc_text_width(s)
    print(f"{s:16s}: Calc={w_c} | Actual={w_actual} | Diff={w_c - w_actual}")
