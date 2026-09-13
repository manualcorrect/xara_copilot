from collect_font_samples import all_samples

chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', ',', '-', '+']
char_to_idx = {c: i for i, c in enumerate(chars)}
n_vars = len(chars)

# Only complete strings ending with ',00'
complete_samples = []
for txt, w in all_samples:
    if txt.endswith(',00') and all(c in char_to_idx for c in txt):
        complete_samples.append((txt, w))

print(f"Complete samples ending with ',00': {len(complete_samples)}")
for txt, w in sorted(complete_samples, key=lambda x: len(x[0])):
    print(f"  {txt:18s} : {w:6d} mp")

# Build Normal Equations
ATA = [[0.0] * n_vars for _ in range(n_vars)]
ATb = [0.0] * n_vars

for txt, w in complete_samples:
    counts = [txt.count(c) for c in chars]
    for i in range(n_vars):
        ATb[i] += counts[i] * w
        for j in range(n_vars):
            ATA[i][j] += counts[i] * counts[j]

# Gaussian elimination with partial pivoting
M = [ATA[i] + [ATb[i]] for i in range(n_vars)]

for i in range(n_vars):
    max_row = i
    for r in range(i + 1, n_vars):
        if abs(M[r][i]) > abs(M[max_row][i]):
            max_row = r
    M[i], M[max_row] = M[max_row], M[i]
    
    pivot = M[i][i]
    if abs(pivot) < 1e-9:
        continue
    for j in range(i, n_vars + 1):
        M[i][j] /= pivot
    for r in range(n_vars):
        if r != i:
            factor = M[r][i]
            for j in range(i, n_vars + 1):
                M[r][j] -= factor * M[i][j]

res = [M[i][n_vars] for i in range(n_vars)]

print("\nFitted Glyph Widths (millipoints):")
for c, w in zip(chars, res):
    print(f"  '{c}': {w:7.2f} mp ({w/28346.4567:.4f} cm)")

# Verify residuals
print("\nPredictions vs Actual:")
max_err = 0
for txt, w in complete_samples:
    pred = sum(txt.count(c) * res[char_to_idx[c]] for c in txt)
    err = abs(pred - w)
    if err > max_err:
        max_err = err
    if err > 100:
        print(f"  {txt:18s} : actual={w}, pred={pred:.0f}, diff={pred-w:.0f}")

print(f"\nMax prediction error: {max_err:.1f} mp ({max_err/28346.4567:.4f} cm)")
