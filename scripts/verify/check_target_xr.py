import struct
from xar_dom_engine import XarDocument

path = r"C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Ananda\New folder\Jul\0.xar"
doc = XarDocument(path)

GLYPH_WIDTHS = {
    '0': 5438, '1': 3160, '2': 4762, '3': 4840, '4': 5039,
    '5': 4840, '6': 4878, '7': 4402, '8': 4962, '9': 4878,
    '.': 1840, ',': 1243, '-': 3198, '+': 4399, ' ': 2200
}

def calc_text_width(text):
    return sum(GLYPH_WIDTHS.get(c, 0) for c in text)

# Check Row 3 (Rec 1912 Saldo, Rec 1933 Nominal)
# Saldo Pos (Rec 1897), Kern (Rec 1911)
s_pos = struct.unpack('<iii', doc.records[1897]['payload'][:12])[0]
s_txt = doc.records[1912]['payload'].decode('utf-16le')
s_kern = struct.unpack('<iii', doc.records[1911]['payload'][:12])[0]
print(f"Row 3 Saldo: pos={s_pos}, txt={repr(s_txt)}, calc_w={calc_text_width(s_txt)}, kern={s_kern}, XR={s_pos + s_kern}")

# Nominal Pos (Rec 1916), Kern (Rec 1932)
n_pos = struct.unpack('<iii', doc.records[1916]['payload'][:12])[0]
n_txt = doc.records[1933]['payload'].decode('utf-16le')
n_kern = struct.unpack('<iii', doc.records[1932]['payload'][:12])[0]
print(f"Row 3 Nominal: pos={n_pos}, txt={repr(n_txt)}, calc_w={calc_text_width(n_txt)}, kern={n_kern}, XR={n_pos + n_kern}")

# Check Row 6 (Rec 2403 Saldo, Rec 2424 Nominal)
s_pos6 = struct.unpack('<iii', doc.records[2388]['payload'][:12])[0]
s_txt6 = doc.records[2403]['payload'].decode('utf-16le')
s_kern6 = struct.unpack('<iii', doc.records[2402]['payload'][:12])[0]
print(f"Row 6 Saldo: pos={s_pos6}, txt={repr(s_txt6)}, calc_w={calc_text_width(s_txt6)}, kern={s_kern6}, XR={s_pos6 + s_kern6}")

n_pos6 = struct.unpack('<iii', doc.records[2407]['payload'][:12])[0]
n_txt6 = doc.records[2424]['payload'].decode('utf-16le')
n_kern6 = struct.unpack('<iii', doc.records[2423]['payload'][:12])[0]
print(f"Row 6 Nominal: pos={n_pos6}, txt={repr(n_txt6)}, calc_w={calc_text_width(n_txt6)}, kern={n_kern6}, XR={n_pos6 + n_kern6}")

