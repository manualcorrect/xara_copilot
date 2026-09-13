import os
import sys
import openpyxl
from datetime import datetime
from xar_dom_engine import XarDocument
from smart_date_time_generator import generate_smart_schedule

def execute_tahap6():
    in_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap5.xar'
    out_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\0_tahap6.xar'
    excel_path = r'C:\Users\Lenovo\Downloads\rekening\PT BENDI NASHA NIAGA INDUSTRI\Marsiyah\New folder\jun\Template_Pekerjaan_Xara_Jun.xlsx'

    print("=========================================================================")
    print("   PROJECT V2 TRAINING: TAHAP 6 - PERUBAHAN TANGGAL & JAM TRANSAKSI")
    print("   Target Dokumen: 7 Halaman / 73 Baris Penuh (19.597 records)")
    print(f"   Input File : {in_path}")
    print(f"   Output File: {out_path}")
    print("=========================================================================\n")

    doc = XarDocument(in_path)
    total_recs_before = len(doc.records)
    print(f"[*] Dokumen dimuat: {total_recs_before:,} records")

    # 1. Parse Excel anchors
    wb = openpyxl.load_workbook(excel_path, data_only=True)
    ws = wb['Tabel_Mutasi']
    anchors = {}
    for r in range(6, 79):
        idx = r - 6
        raw_d = ws.cell(r, 2).value
        raw_t = ws.cell(r, 3).value
        entry = {}
        if raw_d:
            if isinstance(raw_d, datetime):
                if raw_d.month == 6:
                    d_num = min(30, max(1, raw_d.day))
                    entry['date'] = f"2026-06-{d_num:02d}"
            elif '/' in str(raw_d):
                p = str(raw_d).strip().split('/')
                d_num = min(30, max(1, int(p[0])))
                entry['date'] = f"2026-06-{d_num:02d}"
        if raw_t:
            t_str = str(raw_t).strip()
            if 'WIB' not in t_str:
                t_str += ' WIB'
            entry['time'] = t_str
        if entry:
            anchors[idx] = entry

    # Generate 73 rows schedule
    sched = generate_smart_schedule(73, period_start="2026-06-01", period_end="2026-06-30", manual_anchors=anchors)
    print(f"[*] Smart Schedule 73 baris berhasil dibangkitkan (Bulan Jun 2026, 06:00 - 23:00 WIB)")

    # Exact Date and Time records for all 73 rows
    # Format: row_no: {'date': [recs], 'time': [recs]}
    row_starts = {
        1: 1568, 2: 1713, 3: 1853, 4: 2003, 5: 2158, 6: 2298, 7: 2448, 8: 2593, 9: 2733, 10: 2883,
        11: 3962, 12: 4128, 13: 4278, 14: 4418, 15: 4568, 16: 4713, 17: 4858, 18: 5013, 19: 5182, 20: 5332, 21: 5467, 22: 5627,
        23: 6716, 24: 6856, 25: 6996, 26: 7151, 27: 7308, 28: 7448, 29: 7588, 30: 7756, 31: 7919, 32: 8069, 33: 8219, 34: 8369,
        35: 9468, 36: 9618, 37: 9766, 38: 9921, 39: 10066, 40: 10224, 41: 10386, 42: 10531, 43: 10676, 44: 10831, 45: 10976, 46: 11124,
        47: 12240, 48: 12388, 49: 12538, 50: 12678, 51: 12833, 52: 12983, 53: 13123, 54: 13276, 55: 13426, 56: 13576, 57: 13716, 58: 13878,
        59: 14978, 60: 15123, 61: 15263, 62: 15431, 63: 15592, 64: 15747, 65: 15897, 66: 16037, 67: 16204, 68: 16363, 69: 16535, 70: 16690,
        71: 17858, 72: 18010, 73: 18150
    }

    sorted_rows = sorted(row_starts.keys())

    for idx, r_num in enumerate(sorted_rows):
        start = row_starts[r_num]
        end = row_starts[sorted_rows[idx+1]] if idx + 1 < len(sorted_rows) else 18350
        txts = []
        for i in range(start, min(start + 180, end)):
            r = doc.records[i]
            if r['tag'] in (2201, 2202):
                txt = r['payload'].decode('utf-16le', errors='ignore').rstrip('\x00').strip()
                if txt:
                    txts.append((i, r['tag'], txt))

        target_date_str = sched[idx]['date_full'] # e.g. "01 Jun 2026"
        target_time_str = sched[idx]['time']      # e.g. "14:49:21 WIB"
        day_str = target_date_str[:2]

        # Apply Date
        if r_num == 1:
            doc.records[1638]['payload'] = bytearray(day_str[0].encode('utf-16le'))
            doc.records[1638]['size'] = 2
            doc.records[1642]['payload'] = bytearray(day_str[1].encode('utf-16le'))
            doc.records[1642]['size'] = 2
            doc.records[1647]['payload'] = bytearray(" Jun 2026 ".encode('utf-16le'))
            doc.records[1647]['size'] = len(doc.records[1647]['payload'])
        else:
            # Find single date record in txts
            for t in txts:
                if any(m in t[2] for m in ['Jan 2026']) and 'WIB' not in t[2] and 'Periode' not in t[2] and 'Dicetak' not in t[2] and 'dari' not in t[2] and 'DANA' not in t[2]:
                    d_idx = t[0]
                    p = bytearray(target_date_str.encode('utf-16le'))
                    doc.records[d_idx]['payload'] = p
                    doc.records[d_idx]['size'] = len(p)
                    break

        # Apply Time
        t_nodes = [t for t in txts if 'WIB' in t[2] or t[2] in ('WIB', 'WI', 'B') or (':' in t[2] and len(t[2]) >= 5 and any(c.isdigit() for c in t[2]))]
        if len(t_nodes) == 1:
            t_idx = t_nodes[0][0]
            p = bytearray(target_time_str.encode('utf-16le'))
            doc.records[t_idx]['payload'] = p
            doc.records[t_idx]['size'] = len(p)
        elif len(t_nodes) >= 2:
            idx1 = t_nodes[0][0]
            idx2 = t_nodes[1][0]
            orig1_len = len(t_nodes[0][2])
            part1 = target_time_str[:orig1_len]
            part2 = target_time_str[orig1_len:]
            doc.records[idx1]['payload'] = bytearray(part1.encode('utf-16le'))
            doc.records[idx1]['size'] = len(doc.records[idx1]['payload'])
            doc.records[idx2]['payload'] = bytearray(part2.encode('utf-16le'))
            doc.records[idx2]['size'] = len(doc.records[idx2]['payload'])

        if r_num in [1, 10, 20, 30, 40, 50, 60, 70, 73]:
            print(f"[*] Row {r_num:2d}: Tanggal -> '{target_date_str}', Jam -> '{target_time_str}'")

    # Auto-sync all record sizes (Mandatory technical mandate)
    for r in doc.records:
        r['size'] = len(r['payload'])

    # Save to out_path
    doc.save(out_path)
    total_recs_after = len(doc.records)
    print(f"\n[SUCCESS] Tahap 6 Selesai 100%! Output tersimpan di: {out_path}")
    print(f"[*] Zero-Shift Check: {total_recs_before:,} -> {total_recs_after:,} (Status: {total_recs_before == total_recs_after})")

if __name__ == '__main__':
    execute_tahap6()
