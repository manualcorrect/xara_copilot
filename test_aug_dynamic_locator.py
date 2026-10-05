import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\bahan\New folder\Aug\0.xar")

def find_preceding_tag(doc, idx, target_tag, min_size, max_lookback=40):
    for j in range(idx - 1, max(0, idx - max_lookback), -1):
        r = doc.records[j]
        if r['tag'] == target_tag and len(r['payload']) >= min_size:
            return j
    return None

# Test on all 34 rows nominal & saldo
nom_records = [
    1529, 1686, 1844, 2021, 2198, 2387, 2544, 2731, 2888, 3078,
    4045, 4190, 4362, 4529, 4687, 4844, 5012, 5185, 5357, 5534, 5732, 5890,
    6942, 7095, 7248, 7446, 7604, 7757, 7920, 8073, 8241, 8398, 8556, 8718
]

saldo_records = [
    1549, 1706, 1864, 2041, 2218, 2412, 2574, 2751, 2908, 3103,
    4070, 4210, 4392, 4549, 4707, 4864, 5032, 5205, 5377, 5559, 5752, 5910,
    6962, 7115, 7268, 7471, 7629, 7777, 7940, 8098, 8261, 8418, 8576, 8738
]

print("=== VERIFYING DYNAMIC TAG FINDER FOR ALL 34 ROWS ===")
for r_no in range(1, 35):
    nom_idx = nom_records[r_no - 1]
    saldo_idx = saldo_records[r_no - 1]
    
    m_nom = find_preceding_tag(doc, nom_idx, 2100, 12)
    k_nom = find_preceding_tag(doc, nom_idx, 2206, 12)
    c_nom = find_preceding_tag(doc, nom_idx, 150, 4)
    
    m_sal = find_preceding_tag(doc, saldo_idx, 2100, 12)
    k_sal = find_preceding_tag(doc, saldo_idx, 2206, 12)
    c_sal = find_preceding_tag(doc, saldo_idx, 150, 4)
    
    print(f"Row {r_no:02d}: Nom(m={m_nom}, k={k_nom}, c={c_nom}) | Saldo(m={m_sal}, k={k_sal}, c={c_sal})")
    assert all(x is not None for x in [m_nom, k_nom, c_nom, m_sal, k_sal, c_sal]), f"Failed on row {r_no}!"

print("\nALL 34 ROWS DYNAMICALLY RESOLVED 100% PERFECTLY!")
