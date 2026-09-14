"""
CHRONOLOGICAL DATE & TIME ENGINE (UNIVERSAL LOCAL SOLVER)
Solusi Urutan Tanggal & Jam Universal untuk Seluruh Bulan & Dataset Xara.

Prinsip Kerja:
1. Pengguna dapat mengosongkan 99% kolom Tanggal & Jam di Excel dan HANYA mengisi baris tertentu (Anchor).
2. Engine mengekstrak seluruh Anchor eksplisit dari Excel.
3. Menggunakan Piecewise-Monotonic Interpolation dengan Baseline-Shape Preservation:
   - Menjaga proporsi distribusi tanggal asli template dasar (0.xar).
   - Memastikan tidak ada tanggal yang mundur (Monotonic Non-Decreasing: Date[k] >= Date[k-1]).
   - Bidirectional Clamping menjamin seluruh Anchor tanggal tercapai dengan presisi 100%.
4. Mendukung format tanggal/waktu apapun (datetime, time, string, dsb.) secara otomatis.
"""

import calendar
import datetime
from typing import Dict, List, Optional, Tuple, Any

MONTH_NAMES_ID = {
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'Mei', 6: 'Jun',
    7: 'Jul', 8: 'Agt', 9: 'Sep', 10: 'Okt', 11: 'Nov', 12: 'Des'
}

MONTH_MAP_EN_ID = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'mei': 5,
    'jun': 6, 'jul': 7, 'aug': 8, 'agt': 8, 'sep': 9, 'oct': 10,
    'okt': 10, 'nov': 11, 'dec': 12, 'des': 12
}

def parse_month_year(month_year_str: str) -> Tuple[int, int, str]:
    """
    Mengurai string bulan dan tahun (misal: 'Jun 2026', '01 Jun 2026 - 30 Jun 2026')
    menjadi (month, year, label_str).
    """
    s = month_year_str.lower()
    year = 2026
    month = 6
    for word in s.replace('-', ' ').replace('/', ' ').split():
        if word.isdigit() and len(word) == 4:
            year = int(word)
        elif word[:3] in MONTH_MAP_EN_ID:
            month = MONTH_MAP_EN_ID[word[:3]]
    
    month_name = MONTH_NAMES_ID.get(month, 'Jun')
    label_str = f"{month_name} {year}"
    return month, year, label_str

def solve_chronological_dates(
    num_rows: int,
    excel_date_overrides: List[Any],
    baseline_day_numbers: List[int],
    target_month: int = 6,
    target_year: int = 2026,
    month_label: str = "Jun 2026"
) -> List[str]:
    """
    Menghitung urutan tanggal yang 100% kronologis monoton naik untuk num_rows transaksi.
    """
    _, max_days = calendar.monthrange(target_year, target_month)
    
    # 1. Ekstrak Anchor Eksplisit dari Excel
    anchors: Dict[int, int] = {}
    for idx, dt_val in enumerate(excel_date_overrides):
        if dt_val is not None:
            if isinstance(dt_val, (datetime.datetime, datetime.date)):
                anchors[idx] = dt_val.day
            elif isinstance(dt_val, str) and dt_val.strip():
                # parse string seperti '25/06/2026' atau '25-06-2026' atau '25 Jun 2026'
                cleaned = dt_val.strip().replace('-', ' ').replace('/', ' ')
                parts = cleaned.split()
                if parts and parts[0].isdigit():
                    anchors[idx] = max(1, min(max_days, int(parts[0])))

    # Pastikan Anchor Awal & Akhir ada
    if 0 not in anchors:
        anchors[0] = baseline_day_numbers[0] if baseline_day_numbers else 1
    last_idx = num_rows - 1
    if last_idx not in anchors:
        anchors[last_idx] = baseline_day_numbers[-1] if baseline_day_numbers else max_days

    # 2. Piecewise Interpolation Antar-Anchor
    sorted_anchors = sorted(anchors.items())
    final_days = [None] * num_rows

    for i in range(len(sorted_anchors) - 1):
        idx_a, day_a = sorted_anchors[i]
        idx_b, day_b = sorted_anchors[i + 1]
        
        final_days[idx_a] = day_a
        final_days[idx_b] = day_b
        
        if idx_b <= idx_a:
            continue
            
        base_a = baseline_day_numbers[idx_a] if idx_a < len(baseline_day_numbers) else 1
        base_b = baseline_day_numbers[idx_b] if idx_b < len(baseline_day_numbers) else max_days
        
        for k in range(idx_a + 1, idx_b):
            if base_b > base_a and k < len(baseline_day_numbers):
                t = (baseline_day_numbers[k] - base_a) / (base_b - base_a)
            else:
                t = (k - idx_a) / (idx_b - idx_a)
            interp_day = round(day_a + t * (day_b - day_a))
            final_days[k] = max(1, min(max_days, interp_day))

    # 3. Forward Clamp: Menjamin Monoton Naik (Date[k] >= Date[k-1])
    for k in range(1, num_rows):
        if final_days[k] is None or final_days[k] < final_days[k - 1]:
            final_days[k] = final_days[k - 1]
            
    # 4. Backward Clamp: Menjamin Anchor Target Tidak Dilanggar (Date[k] <= Date[k+1])
    for k in range(num_rows - 2, -1, -1):
        if final_days[k] > final_days[k + 1]:
            final_days[k] = final_days[k + 1]

    # 5. Format Menjadi String Tanggal Resmi Xara
    formatted_dates = []
    for d in final_days:
        formatted_dates.append(f"{d:02d} {month_label}")
        
    return formatted_dates

def solve_synchronized_times(
    num_rows: int,
    solved_dates: List[str],
    excel_time_overrides: List[Any],
    baseline_times: List[str],
    min_hour: int = 6,
    max_hour: int = 23
) -> List[str]:
    """
    Sinkronisasi Jam & Tanggal secara Logis (06:00 - 23:00):
    1. Mengelompokkan transaksi per tanggal yang sama.
    2. Menjamin urutan jam dalam satu tanggal selalu monoton naik (T[k] >= T[k-1]).
    3. Memetakan seluruh transaksi normal ke jam aktif yang logis (06:00 - 23:00).
    4. Mempertahankan jam tutup buku akhir bulan (misal 23:59:00 WIB).
    """
    def parse_to_sec(t_val):
        if t_val is None:
            return None
        if isinstance(t_val, datetime.time):
            return t_val.hour * 3600 + t_val.minute * 60 + t_val.second
        if isinstance(t_val, (datetime.datetime, datetime.date)):
            return t_val.hour * 3600 + t_val.minute * 60 + t_val.second
        s = str(t_val).replace('WIB', '').replace('WI', '').replace('W', '').replace('IB', '').strip()
        parts = s.split(':')
        if len(parts) >= 2:
            try:
                h = int(parts[0])
                m = int(parts[1])
                sec = int(parts[2]) if len(parts) >= 3 and parts[2].isdigit() else 0
                return h * 3600 + m * 60 + sec
            except:
                pass
        return None

    def sec_to_str(secs):
        secs = max(0, min(86399, int(secs)))
        h = secs // 3600
        m = (secs % 3600) // 60
        s = secs % 60
        return f"{h:02d}:{m:02d}:{s:02d} WIB"

    min_sec = min_hour * 3600                  # 06:00:00 -> 21,600 detik
    max_sec = (max_hour - 1) * 3600 + 55 * 60  # 22:55:00 -> 82,500 detik

    # Kelompokkan per tanggal
    date_groups: Dict[str, List[int]] = {}
    for idx, d_str in enumerate(solved_dates):
        date_groups.setdefault(d_str, []).append(idx)

    final_times: List[Optional[str]] = [None] * num_rows

    for d_str, indices in date_groups.items():
        m = len(indices)
        raw_secs = []
        for pos, idx in enumerate(indices):
            tm_ov = excel_time_overrides[idx] if idx < len(excel_time_overrides) else None
            sec_ov = parse_to_sec(tm_ov)
            if sec_ov is not None:
                # Cek khusus transaksi penutupan / admin fee akhir bulan
                if idx == num_rows - 1 and sec_ov >= 23 * 3600:
                    raw_secs.append(sec_ov)
                else:
                    clamped_ov = max(min_sec, min(max_sec, sec_ov))
                    raw_secs.append(clamped_ov)
            else:
                base_sec = parse_to_sec(baseline_times[idx]) if idx < len(baseline_times) else None
                if base_sec is None:
                    base_sec = min_sec + pos * 1800
                if base_sec < min_sec:
                    # Geser waktu subuh/dini hari ke jam kerja siang (+6 jam mod 4 jam)
                    base_sec = min_sec + (base_sec % (4 * 3600))
                clamped_base = max(min_sec, min(max_sec, base_sec))
                raw_secs.append(clamped_base)

        # Urutkan detik secara strictly non-decreasing dalam satu tanggal
        raw_secs.sort()
        for pos in range(len(raw_secs)):
            idx = indices[pos]
            if pos > 0 and raw_secs[pos] < raw_secs[pos - 1]:
                raw_secs[pos] = raw_secs[pos - 1] + 15
            final_times[idx] = sec_to_str(raw_secs[pos])

    return [t or "08:00:00 WIB" for t in final_times]
