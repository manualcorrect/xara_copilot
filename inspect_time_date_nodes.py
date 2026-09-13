import struct
from xar_dom_engine import XarDocument

doc = XarDocument(r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Firmansyah\New folder\Jul\0.xar')

# Inspect all text nodes between saldo and date for each row
nom_recs = [1587, 1778, 1949, 2115, 2316, 2477, 2643, 2823, 3014, 3192,
            4215, 4401, 4587, 4753, 4929, 5114, 5300, 5471, 5632, 5808, 5994, 6160]

for idx, n_idx in enumerate(nom_recs, 1):
    # Find text nodes between n_idx + 10 and n_idx + 80
    time_nodes = []
    date_node = None
    for j in range(n_idx + 5, n_idx + 90):
        if j >= len(doc.records): break
        r = doc.records[j]
        if r['tag'] in (2201, 2202):
            try:
                t = r['payload'].decode('utf-16le').rstrip('\x00')
                if 'Nov' in t or '2025' in t or 'Des' in t:
                    date_node = (j, r['tag'], t)
                    break
                elif any(c.isdigit() for c in t) or 'WIB' in t or ':' in t:
                    time_nodes.append((j, r['tag'], t))
            except:
                pass
    print(f"Row {idx:2d}: Date={date_node} | Time={time_nodes}")
