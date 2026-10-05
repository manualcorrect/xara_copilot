with open('all_rows_text_utf8.txt', 'rb') as f:
    raw = f.read()

txt = raw.decode('utf-16le' if raw.startswith(b'\xff\xfe') else 'utf-8', errors='ignore')
with open('all_rows_text_clean.txt', 'w', encoding='utf-8') as out:
    out.write(txt)

print("Saved all_rows_text_clean.txt")
