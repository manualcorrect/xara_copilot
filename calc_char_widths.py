# Pure Python linear regression to find character widths
from xar_dom_engine import XarDocument
import struct

doc = XarDocument(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar")

# Let's inspect the exact glyph widths
# In Xar format, Tag 2200 or font records define the font metrics!
# Where are font definitions in Xar format?
# Tag 176 / 177 / 2901 / 2906 / 2907 etc.
# But we can also solve using the full samples:
samples = [
    ("-50.000,00", 43337),
    ("970.834,00", 42848),
    ("-8.000,00", 38065),
    ("1.018.834,00", 46673),
    ("738.834,00", 42521),
    ("-6.500,00", 37380),
    ("+41.000,00", 42291),
    ("10.000,00", 41650),
]

# Let's see: if all digits (0-9) have width W_digit, '.' and ',' have W_punct, '-' has W_minus, '+' has W_plus
# Row 1: -50.000,00 -> 1 minus, 7 digits, 2 dots/commas
# Row 4: -8.000,00  -> 1 minus, 6 digits, 2 dots/commas
# Difference: Row 1 - Row 4 = 1 digit = 43337 - 38065 = 5272 millipoints!
# Row 8: +41.000,00 -> 1 plus, 7 digits, 2 dots/commas = 42291
# Row 10.000,00     -> 0 sign, 7 digits, 2 dots/commas = 41650
# Minus sign: -50.000,00 (43337) - 10.000,00 (41650) = 1687 millipoints!
# Plus sign:  +41.000,00 (42291) - 10.000,00 (41650) = 641 millipoints!
# Digit width:
# 1.018.834,00 has 9 digits, 3 punct = 46673
# 738.834,00 has 8 digits, 2 punct = 42521
# Difference: 1 digit + 1 punct = 46673 - 42521 = 4152 millipoints!
w_digit = 43337 - 38065 # 5272? wait, -50.000,00 has 7 digits, -8.000,00 has 6 digits
print("Difference (1 digit):", 43337 - 38065)
print("Difference (1.018.834,00 - 970.834,00):", 46673 - 42848) # 2 digits (1.0 vs 9): 3825 millipoints
