from collect_font_samples import all_samples

# Let's find pairs of complete samples that differ by simple substitutions
# For example:
# -1.000.000,00 vs -500.000,00 vs -200.000,00 vs -100.000,00
# 5.434.083,00 vs 5.364.083,00 vs 5.363.583,00
print("=== EXACT PAIR DIFFERENCES ===")
for s1, w1 in all_samples:
    for s2, w2 in all_samples:
        if len(s1) == len(s2) and s1 != s2 and s1.endswith(',00') and s2.endswith(',00'):
            # count differing characters
            diffs = [(c1, c2) for c1, c2 in zip(s1, s2) if c1 != c2]
            if len(diffs) == 1:
                c1, c2 = diffs[0]
                print(f"'{s1}' ({w1}) vs '{s2}' ({w2}) -> '{c1}' - '{c2}' = {w1 - w2} mp")
            elif len(diffs) == 2 and diffs[0][0] == diffs[1][1] and diffs[0][1] == diffs[1][0]:
                pass

