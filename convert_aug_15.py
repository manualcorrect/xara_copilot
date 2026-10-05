with open('aug_15_rows_raw.txt', 'rb') as f:
    raw = f.read()

txt = raw.decode('utf-16le' if raw.startswith(b'\xff\xfe') else 'utf-8', errors='ignore')
with open('aug_15_rows_clean.txt', 'w', encoding='utf-8') as out:
    out.write(txt)

print("Saved aug_15_rows_clean.txt")
