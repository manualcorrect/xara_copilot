with open('all_aug_rows.txt', 'rb') as f:
    raw = f.read()

txt = raw.decode('utf-16le' if raw.startswith(b'\xff\xfe') else 'utf-8', errors='ignore')
with open('all_aug_rows_utf8.txt', 'w', encoding='utf-8') as out:
    out.write(txt)

print("Saved all_aug_rows_utf8.txt")
