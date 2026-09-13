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

A = []
B = []
for s, w in samples:
    d_cnt = sum(c.isdigit() for c in s)
    p_cnt = s.count('.') + s.count(',')
    m_cnt = s.count('-')
    plus_cnt = s.count('+')
    A.append([d_cnt, p_cnt, m_cnt, plus_cnt])
    B.append(w)

# Normal equations: (A^T A) x = A^T B
ATA = [[sum(A[k][i] * A[k][j] for k in range(len(A))) for j in range(4)] for i in range(4)]
ATB = [sum(A[k][i] * B[k] for k in range(len(A))) for i in range(4)]

# Solve 4x4 using Gaussian elimination
M = [ATA[i] + [ATB[i]] for i in range(4)]
for i in range(4):
    pivot = M[i][i]
    for j in range(i, 5):
        M[i][j] /= pivot
    for k in range(4):
        if k != i:
            factor = M[k][i]
            for j in range(i, 5):
                M[k][j] -= factor * M[i][j]

res = [M[i][4] for i in range(4)]
print("Fitted glyph widths (pure python):")
print(f"  Digit:         {res[0]:.1f} millipoints")
print(f"  Punct (. / ,): {res[1]:.1f} millipoints")
print(f"  Minus (-):     {res[2]:.1f} millipoints")
print(f"  Plus (+):      {res[3]:.1f} millipoints\n")

# Verify predictions:
for s, w in samples:
    d_cnt = sum(c.isdigit() for c in s)
    p_cnt = s.count('.') + s.count(',')
    m_cnt = s.count('-')
    plus_cnt = s.count('+')
    pred = d_cnt*res[0] + p_cnt*res[1] + m_cnt*res[2] + plus_cnt*res[3]
    print(f"  {s:15s}: actual={w}, pred={pred:.0f}, diff={pred-w:.0f}")

# Now calculate for target:
# Nominal target: "-1.000.000,00"
nom_str = "-1.000.000,00"
d_cnt = sum(c.isdigit() for c in nom_str)
p_cnt = nom_str.count('.') + nom_str.count(',')
m_cnt = nom_str.count('-')
nom_pred_w = int(d_cnt*res[0] + p_cnt*res[1] + m_cnt*res[2])
print(f"\nTarget Nominal '{nom_str}': predicted width = {nom_pred_w}")

# Balance target: "15.927.222,00"
bal_str = "15.927.222,00"
d_cnt = sum(c.isdigit() for c in bal_str)
p_cnt = bal_str.count('.') + bal_str.count(',')
bal_pred_w = int(d_cnt*res[0] + p_cnt*res[1])
print(f"Target Balance '{bal_str}': predicted width = {bal_pred_w}")
