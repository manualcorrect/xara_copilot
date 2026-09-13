import struct
import zlib

src_path = r"C:\Users\Lenovo\Downloads\TEST_REK_ANTIGRAVITY.xar"
with open(src_path, "rb") as f:
    data = f.read()

comp_pos = 0x5594
tag, size = struct.unpack_from("<II", data, comp_pos)
compressed_data = data[comp_pos + 8 + size:]

cur = compressed_data
stream_idx = 0
streams = []
while len(cur) > 32:
    try:
        d = zlib.decompressobj(-15)
        chunk = d.decompress(cur)
        if chunk:
            stream_idx += 1
            consumed = len(cur) - len(d.unused_data)
            streams.append(chunk)
            cur = d.unused_data
            while len(cur) > 0 and cur[0] == 0:
                cur = cur[1:]
        else:
            cur = cur[1:]
    except Exception:
        cur = cur[1:]

s5 = streams[4]
pos = 0
recs = []
while pos + 8 <= len(s5):
    t, sz = struct.unpack_from("<II", s5, pos)
    payload = s5[pos+8 : pos+8+sz]
    recs.append((pos, t, sz, payload))
    pos += 8 + sz

print(f"Stream 5: total records={len(recs)}, exact coverage={pos == len(s5)}")

with open(r"C:\Users\Lenovo\xara_copilot\stream5_records.txt", "w", encoding="utf-8") as out:
    for i, (p, t, sz, payload) in enumerate(recs):
        txt = ""
        if t == 0x899:
            txt = payload.decode("utf-16le", errors="replace")
        elif t == 0x898:
            txt = payload.decode("latin1", errors="replace")
        elif t == 0x89E:
            coords = struct.unpack(f"<{len(payload)//4}i", payload[:(len(payload)//4)*4])
            txt = f"COORDS: {coords}"
        elif t == 0x89A:
            txt = f"CHAR_UNICODE: {payload.decode('utf-16le', errors='replace')}"
        if txt:
            out.write(f"[{i:4d}] 0x{p:05X} Tag=0x{t:04X} ({t:4d}) Size={sz:3d} : {txt}\n")

print("Saved stream5_records.txt")
