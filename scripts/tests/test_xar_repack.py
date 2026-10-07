import struct
import zlib
import os

src_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
dst_path = r"C:\Users\Lenovo\Downloads\TEST_REK_EDITED.xar"

with open(src_path, "rb") as f:
    data = f.read()

# Header before compression
comp_pos = 0x5594 # TAG_STARTCOMPRESSION
tag, size = struct.unpack_from("<II", data, comp_pos)
header_bytes = data[:comp_pos + 8 + size]
compressed_data = data[comp_pos + 8 + size:]

# Decompress all data
cur = compressed_data
all_decomp = bytearray()

while len(cur) > 32:
    try:
        d = zlib.decompressobj(-15)
        chunk = d.decompress(cur)
        if chunk:
            all_decomp.extend(chunk)
            unused = d.unused_data
            if len(unused) == len(cur):
                cur = cur[1:]
            else:
                cur = unused
        else:
            cur = cur[1:]
    except Exception:
        cur = cur[1:]

print(f"Header size: {len(header_bytes):,} bytes")
print(f"Decompressed stream size: {len(all_decomp):,} bytes")

# Test editing: let's find '23:05:11 WIB' in all_decomp
find_u16 = '23:05:11 WIB'.encode('utf-16le')
repl_u16 = '01:23:45 WIB'.encode('utf-16le')

idx = all_decomp.find(find_u16)
print(f"Index of '23:05:11 WIB': {idx}")

if idx != -1:
    # Replace in place (both are 12 characters = 24 bytes!)
    all_decomp[idx:idx+len(find_u16)] = repl_u16
    print(f"Successfully replaced '23:05:11 WIB' with '01:23:45 WIB'!")

# Recompress stream using raw deflate (-15)
compressor = zlib.compressobj(6, zlib.DEFLATED, -15)
new_compressed = compressor.compress(all_decomp) + compressor.flush()
print(f"New compressed size: {len(new_compressed):,} bytes (original: {len(compressed_data):,} bytes)")

# Write new .xar file
with open(dst_path, "wb") as f:
    f.write(header_bytes)
    f.write(new_compressed)

print(f"Saved: {dst_path} ({os.path.getsize(dst_path):,} bytes)")
