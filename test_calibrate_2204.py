from xar_dom_engine import XarDocument
import struct

doc0 = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0.xar')

# Exact glyph widths in dx units for digits, comma, period
# We know:
# Row 10: '10' + '2.181.835,81' -> dx=62330, dy=4487760
# Row 11: '11' + '2.179.335,81' -> dx=62545, dy=4503222
# Row 12: '12' + '279.335,81'   -> dx=62940, dy=4531662
# Row 56: '56' + '146.335,81'   -> dx=62810, dy=4522302

# When changing saldo from '146.335,81' (10 chars) to '6.502.335,81' (12 chars):
# '6.502.335,81' is in millions (same format as '2.179.335,81' in Row 11)
# For '56' + '6.502.335,81':
# dx = 62200, dy = round(62200 * 72) = 4478400

print("Ready to calibrate rows 56..73 Tag 2204!")
