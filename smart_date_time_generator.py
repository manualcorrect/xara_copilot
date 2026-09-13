import random
from datetime import datetime, timedelta

def generate_smart_schedule(total_rows, period_start="2026-12-01", period_end="2026-12-31", manual_anchors=None):
    """
    Generates realistic, chronologically sorted dates and times between 06:00 and 23:00.
    manual_anchors: dict of {row_index: {'date': 'YYYY-MM-DD', 'time': 'HH:MM:SS'}}
    """
    if manual_anchors is None:
        manual_anchors = {}
        
    start_dt = datetime.strptime(period_start, "%Y-%m-%d")
    end_dt = datetime.strptime(period_end, "%Y-%m-%d")
    total_days = (end_dt - start_dt).days + 1
    
    # 1. Establish anchor points
    anchors = {0: start_dt}
    for r_idx, val in manual_anchors.items():
        if 'date' in val and val['date']:
            d_obj = datetime.strptime(val['date'], "%Y-%m-%d")
            anchors[r_idx] = d_obj
    anchors[total_rows - 1] = end_dt
    
    sorted_anchor_rows = sorted(anchors.keys())
    
    # 2. Interpolate dates across segments
    schedule_dates = {}
    for i in range(len(sorted_anchor_rows) - 1):
        r_start = sorted_anchor_rows[i]
        r_end = sorted_anchor_rows[i+1]
        d_start = anchors[r_start]
        d_end = anchors[r_end]
        
        seg_len = r_end - r_start
        seg_days = (d_end - d_start).days
        
        for step in range(seg_len + 1):
            curr_row = r_start + step
            if curr_row not in schedule_dates:
                # Linear interpolation with slight natural jitter
                day_offset = int(round(step * seg_days / seg_len)) if seg_len > 0 else 0
                calc_date = d_start + timedelta(days=day_offset)
                schedule_dates[curr_row] = calc_date
                
    # 3. Generate 24-hour human-active times (06:00 - 23:00)
    # Ensure chronological order within the same date
    final_schedule = []
    
    # Group rows by date to assign realistic increasing times
    date_to_rows = {}
    for r in range(total_rows):
        d_str = schedule_dates[r].strftime("%Y-%m-%d")
        if d_str not in date_to_rows:
            date_to_rows[d_str] = []
        date_to_rows[d_str].append(r)
        
    row_times = {}
    for d_str, r_list in date_to_rows.items():
        # Distribute r_list across 06:00 to 22:45
        n = len(r_list)
        # Starting hour between 06:00 and 09:00
        start_min_total = random.randint(6 * 60, 9 * 60)
        # End hour up to 23:00 (1380 mins)
        max_min_total = 23 * 60 - 15
        
        if n == 1:
            m_rand = random.randint(start_min_total, max_min_total)
            row_times[r_list[0]] = f"{m_rand//60:02d}:{m_rand%60:02d}:{random.randint(0, 59):02d} WIB"
        else:
            step = (max_min_total - start_min_total) / max(1, n)
            curr_min = start_min_total
            for idx, r in enumerate(r_list):
                if r in manual_anchors and manual_anchors[r].get('time'):
                    row_times[r] = manual_anchors[r]['time']
                else:
                    m_val = int(curr_min + random.randint(0, max(5, int(step * 0.5))))
                    m_val = min(m_val, max_min_total)
                    row_times[r] = f"{m_val//60:02d}:{m_val%60:02d}:{random.randint(0, 59):02d} WIB"
                    curr_min += step
                    
    for r in range(total_rows):
        d_obj = schedule_dates[r]
        manual_override = r in manual_anchors
        final_schedule.append({
            "row": r + 1,
            "date": d_obj.strftime("%d/%m"),
            "date_full": d_obj.strftime("%d %b %Y"),
            "time": row_times[r],
            "is_manual": manual_override
        })
        
    return final_schedule

if __name__ == "__main__":
    # Test simulation: 47 rows with manual anchors at Row 14 (10 Dec) and Row 35 (25 Dec)
    anchors = {
        13: {'date': '2026-12-10', 'time': '10:00:00 WIB'}, # Row 14 (0-indexed 13)
        34: {'date': '2026-12-25', 'time': '09:00:00 WIB'}  # Row 35 (0-indexed 34)
    }
    res = generate_smart_schedule(47, manual_anchors=anchors)
    print("Simulated Smart Schedule Sample:")
    for row in res[:5]:
        print(f"Row {row['row']:2d}: {row['date']} | {row['time']} | Manual: {row['is_manual']}")
    print("...")
    print(f"Row 14: {res[13]['date']} | {res[13]['time']} | Manual: {res[13]['is_manual']} (ANCHOR)")
    print("...")
    print(f"Row 35: {res[34]['date']} | {res[34]['time']} | Manual: {res[34]['is_manual']} (ANCHOR)")
    print("...")
    for row in res[-3:]:
        print(f"Row {row['row']:2d}: {row['date']} | {row['time']} | Manual: {row['is_manual']}")
