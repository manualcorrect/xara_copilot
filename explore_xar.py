import struct
import zlib
import re

with open(r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar", "rb") as f:
    data = f.read()

cur_data = data[0x5594+12:]
all_decompressed = bytearray()

while len(cur_data) > 32:
    try:
        d = zlib.decompressobj(-15)
        chunk = d.decompress(cur_data)
        if chunk:
            all_decompressed.extend(chunk)
            unused = d.unused_data
            if len(unused) == len(cur_data):
                cur_data = cur_data[1:]
            else:
                cur_data = unused
        else:
            cur_data = cur_data[1:]
    except Exception:
        cur_data = cur_data[1:]

print("Searching offset of '23:05:11' in all_decompressed...")
target_asc = b'23:05:11'
target_u16 = '23:05:11'.encode('utf-16le')

idx_asc = all_decompressed.find(target_asc)
idx_u16 = all_decompressed.find(target_u16)

print(f"ASCII index: {idx_asc}, UTF16 index: {idx_u16}")

idx = idx_asc if idx_asc != -1 else idx_u16
if idx != -1:
    print("Found! Context around target:")
    start = max(0, idx - 40)
    end = min(len(all_decompressed), idx + 50)
    raw_ctx = all_decompressed[start:end]
    print("Raw bytes:", raw_ctx)
    print("Latin1:", raw_ctx.decode('latin1', errors='replace'))
    try:
        print("UTF-16LE:", raw_ctx.decode('utf-16le', errors='replace'))
    except:
        pass
