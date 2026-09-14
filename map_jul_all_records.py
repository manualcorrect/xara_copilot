import json
import struct
from xar_dom_engine import XarDocument

xar_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jul\0.xar'
doc = XarDocument(xar_path)
total_recs = len(doc.records)
print(f"Total records in 0.xar: {total_recs:,}")

mapping = {
    "customer_name": [],
    "period": [],
    "dicetak_pada": [],
    "account_number": None,
    "page_numbers": [],
    "financial_summary": {},
    "rows": []
}

# 1. Customer Name (8 pages)
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if 'ROY DARWIN' in t:
            mapping["customer_name"].append({"rec_idx": i, "tag": r['tag'], "text": t, "kern_idx": i - 1 if doc.records[i-1]['tag'] == 2206 else None})

# 2. Period (8 pages)
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if 'Feb 2026 - 28 Feb 202' in t:
            mapping["period"].append({"rec_idx": i, "tag": r['tag'], "text": t})

# 3. Dicetak Pada (8 pages)
for i, r in enumerate(doc.records):
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if 'Sep 2026' in t and (i in [1057, 3702, 6486, 9210, 11930, 14706, 17449, 20249] or len(mapping["dicetak_pada"]) < 8):
            mapping["dicetak_pada"].append({"rec_idx": i, "tag": r['tag'], "text": t})

# 4. Account Number
for i in range(1000, 1100):
    r = doc.records[i]
    if r['tag'] in (2201, 2202):
        t = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
        if '1650003584860' in t:
            mapping["account_number"] = {"rec_idx": i, "tag": r['tag'], "text": t}

# 5. Financial Summary
mapping["financial_summary"] = {
    "saldo_awal": {"rec_idx": 1175, "text": "21.347,81 "},
    "dana_masuk_p1": {"rec_idx": 1184, "text": "+ 11.086.00"},
    "dana_masuk_p2": {"rec_idx": 1189, "text": "0,00"},
    "dana_keluar": {"rec_idx": 1202, "text": "- 9.608.579,00 "},
    "saldo_akhir": {"rec_idx": 1215, "text": "1.498.768,81"}
}

# 6. Map all 83 transaction rows
# In 0.xar, each row has a row number (e.g. 1..83), followed by Tag 2204, then Saldo
# Before row number or around it, there is Date, Time, Description, Nominal
# Let's find all rows systematically
for i in range(len(doc.records)):
    r = doc.records[i]
    if r['tag'] == 2204 and i + 6 < len(doc.records):
        for k in range(i+1, min(len(doc.records), i+10)):
            rk = doc.records[k]
            if rk['tag'] in (2201, 2202):
                txt = rk['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                if ',' in txt and (txt.endswith(',81') or txt.endswith(',00')) and not txt.startswith('0'):
                    # Row number is before Tag 2204
                    row_no_rec = None
                    row_no_val = None
                    for p in range(max(0, i-6), i):
                        if doc.records[p]['tag'] in (2201, 2202):
                            r_txt = doc.records[p]['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                            if r_txt.isdigit():
                                row_no_rec = p
                                row_no_val = int(r_txt)
                                break
                    if row_no_rec:
                        # Find nominal after saldo
                        nom_rec = None
                        nom_val = None
                        nom_tag2206 = None
                        nom_tag2100 = None
                        nom_color = None
                        for n in range(k+1, min(len(doc.records), k+40)):
                            rn = doc.records[n]
                            if rn['tag'] in (2201, 2202):
                                n_txt = rn['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                if (n_txt.startswith('-') or n_txt.startswith('+')) and ',' in n_txt:
                                    nom_rec = n
                                    nom_val = n_txt
                                    # find Tag 2206 before nom_rec
                                    for t6 in range(max(0, n-5), n):
                                        if doc.records[t6]['tag'] == 2206:
                                            nom_tag2206 = t6
                                            break
                                    # find Tag 2100 before nom_rec
                                    for t1 in range(max(0, n-25), n):
                                        if doc.records[t1]['tag'] == 2100:
                                            nom_tag2100 = t1
                                            break
                                    # find Tag 150 before nom_rec
                                    for c in range(max(0, n-20), n):
                                        if doc.records[c]['tag'] == 150:
                                            nom_color = doc.records[c]['payload'].hex()
                                            break
                                    break
                                    
                        # Find Date and Time before row number
                        date_rec = None
                        date_val = None
                        time_rec = None
                        time_val = None
                        for d in range(max(0, row_no_rec-35), row_no_rec):
                            rd = doc.records[d]
                            if rd['tag'] in (2201, 2202):
                                d_txt = rd['payload'].decode('utf-16le', errors='ignore').rstrip('\x00')
                                if 'Feb 2026' in d_txt and len(d_txt) >= 10:
                                    date_rec = d
                                    date_val = d_txt
                                elif 'WIB' in d_txt or ':' in d_txt and any(c.isdigit() for c in d_txt):
                                    time_rec = d
                                    time_val = d_txt
                                    
                        dx, dy = struct.unpack('<ii', doc.records[i]['payload'][:8])
                        mapping["rows"].append({
                            "row_num": row_no_val,
                            "row_no_rec": row_no_rec,
                            "tag2204_rec": i,
                            "orig_dx": dx,
                            "orig_dy": dy,
                            "saldo_rec": k,
                            "orig_saldo": txt,
                            "nominal_rec": nom_rec,
                            "orig_nominal": nom_val,
                            "nom_tag2206": nom_tag2206,
                            "nom_tag2100": nom_tag2100,
                            "nom_color": nom_color,
                            "date_rec": date_rec,
                            "orig_date": date_val,
                            "time_rec": time_rec,
                            "orig_time": time_val
                        })
                    break

print(f"Total mapped rows: {len(mapping['rows'])}")
with open('jul_mapping.json', 'w', encoding='utf-8') as f:
    json.dump(mapping, f, indent=2)

print("[OK] Mapping saved to jul_mapping.json")
