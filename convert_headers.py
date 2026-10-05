import codecs

with open('headers_detail_out.txt', 'rb') as f:
    raw = f.read()

# Try decode utf-16le then save utf-8
text = raw.decode('utf-16le' if raw.startswith(b'\xff\xfe') else 'utf-8', errors='ignore')

with open('headers_detail_utf8.txt', 'w', encoding='utf-8') as out:
    out.write(text)

print("Saved headers_detail_utf8.txt")
