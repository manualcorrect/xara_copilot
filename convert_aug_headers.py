with open('aug_headers_clean.txt', 'rb') as f:
    raw = f.read()

txt = raw.decode('utf-16le' if raw.startswith(b'\xff\xfe') else 'utf-8', errors='ignore')
with open('aug_headers_utf8.txt', 'w', encoding='utf-8') as out:
    out.write(txt)

print("Saved aug_headers_utf8.txt")
