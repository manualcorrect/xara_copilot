import sqlite3

def decode_protobuf(data, depth=0):
    idx = 0
    res = {}
    while idx < len(data):
        # read varint key
        byte = data[idx]
        idx += 1
        wire_type = byte & 0x07
        field_num = byte >> 3
        
        if wire_type == 0: # varint
            val = 0
            shift = 0
            while True:
                b = data[idx]
                idx += 1
                val |= (b & 0x7F) << shift
                if not (b & 0x80):
                    break
                shift += 7
            res[f"field_{field_num}"] = val
        elif wire_type == 2: # length-delimited
            length = 0
            shift = 0
            while True:
                b = data[idx]
                idx += 1
                length |= (b & 0x7F) << shift
                if not (b & 0x80):
                    break
                shift += 7
            sub_data = data[idx:idx+length]
            idx += length
            if depth < 3:
                try:
                    sub_parsed = decode_protobuf(sub_data, depth+1)
                    res[f"field_{field_num}_msg"] = sub_parsed
                except:
                    res[f"field_{field_num}_bytes"] = sub_data
            else:
                res[f"field_{field_num}_bytes"] = sub_data
        elif wire_type == 1: # 64-bit
            idx += 8
        elif wire_type == 5: # 32-bit
            idx += 4
        else:
            break
    return res

db_path = r'C:\Users\Lenovo\.gemini\antigravity-ide\conversations\7fc1812d-77c0-4729-a186-6403d1a60a1b.db'
conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
cursor = conn.cursor()

cursor.execute("SELECT idx, step_type, metadata FROM steps WHERE metadata IS NOT NULL;")
rows = cursor.fetchall()
print(f"Total steps: {len(rows)}")

found_token_stats = []
for r in rows:
    try:
        parsed = decode_protobuf(r[2])
        # Look for token fields
        found_token_stats.append((r[0], r[1], parsed))
    except Exception as e:
        pass

# Print some decoded metadata
for step_idx, stype, parsed in found_token_stats:
    # search for fields that look like token counts (e.g. > 100)
    def search_keys(d):
        tokens = {}
        for k, v in d.items():
            if isinstance(v, dict):
                tokens.update(search_keys(v))
            elif isinstance(v, int):
                tokens[k] = v
        return tokens
    t = search_keys(parsed)
    # Check if this looks like usage metadata (has field_1, field_2, etc. with numbers)
    for k, v in parsed.items():
        if 'field_9' in k or 'field_8' in k or 'field_10' in k:
            if isinstance(v, dict):
                print(f"Step {step_idx} ({stype}): {k} -> {v}")
