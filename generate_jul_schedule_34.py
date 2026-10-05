import json
from datetime import datetime, timedelta

def build_schedule():
    # 34 rows
    # Start: 01 Jul 2026
    # Row 26 (idx 25): 25 Jul 2026, 04:00:00 WIB
    # Row 34 (idx 33): 31 Jul 2026, 23:59:00 WIB
    
    # Original template dates as base pattern:
    # Page 1 (Rows 1..10): 01 Sep (Rows 1..4), 02 Sep (Rows 5..10)
    # Page 2 (Rows 11..22): 03 Sep (Rows 11..14), 04 Sep (Rows 15..21), 05 Sep (Row 22)
    # Page 3 (Rows 23..34): 05 Sep (Row 23), 06 Sep (Rows 24..31), 08 Sep (Rows 32..34)
    
    # For July 2026 (01 Jul - 31 Jul):
    # Rows 1..4: 01 Jul 2026
    # Rows 5..10: 05 Jul 2026
    # Rows 11..14: 10 Jul 2026
    # Rows 15..21: 17 Jul 2026
    # Rows 22..25: 22 Jul 2026
    # Row 26: 25 Jul 2026 (04:00:00 WIB)
    # Rows 27..30: 27 Jul 2026
    # Rows 31..33: 29 Jul 2026
    # Row 34: 31 Jul 2026 (23:59:00 WIB)

    # Let's verify times to ensure strictly chronological and preserving format
    dates_plan = [
        # Page 1 (Rows 1..10)
        ("01 Jul 2026", "04:12:29 WIB"),
        ("01 Jul 2026", "18:44:56 WIB"),
        ("01 Jul 2026", "20:17:05 WIB"),
        ("01 Jul 2026", "20:51:14 WIB"),
        ("05 Jul 2026", "12:04:48 WIB"),
        ("05 Jul 2026", "15:44:38 WIB"),
        ("05 Jul 2026", "16:14:48 WIB"),
        ("05 Jul 2026", "18:50:21 WIB"),
        ("05 Jul 2026", "20:54:27 WIB"),
        ("05 Jul 2026", "20:59:57 WIB"),
        
        # Page 2 (Rows 11..22)
        ("10 Jul 2026", "09:41:50 WIB"),
        ("10 Jul 2026", "09:43:53 WIB"),
        ("10 Jul 2026", "13:15:49 WIB"),
        ("10 Jul 2026", "15:22:37 WIB"),
        ("17 Jul 2026", "12:18:09 WIB"),
        ("17 Jul 2026", "14:40:58 WIB"),
        ("17 Jul 2026", "16:52:40 WIB"),
        ("17 Jul 2026", "18:21:33 WIB"),
        ("17 Jul 2026", "19:01:50 WIB"),
        ("17 Jul 2026", "20:06:28 WIB"),
        ("17 Jul 2026", "21:43:18 WIB"),
        ("22 Jul 2026", "14:40:47 WIB"),

        # Page 3 (Rows 23..34)
        ("22 Jul 2026", "15:14:55 WIB"),
        ("24 Jul 2026", "06:14:12 WIB"),
        ("24 Jul 2026", "06:18:02 WIB"),
        ("25 Jul 2026", "04:00:00 WIB"), # Explicit Anchor
        ("27 Jul 2026", "07:46:39 WIB"),
        ("27 Jul 2026", "07:55:03 WIB"),
        ("27 Jul 2026", "20:38:12 WIB"),
        ("27 Jul 2026", "21:07:33 WIB"),
        ("28 Jul 2026", "22:50:06 WIB"),
        ("29 Jul 2026", "14:10:44 WIB"),
        ("29 Jul 2026", "16:21:16 WIB"),
        ("31 Jul 2026", "23:59:00 WIB"), # Explicit Anchor
    ]

    schedule = []
    for i, (d, t) in enumerate(dates_plan):
        schedule.append({
            "row_no": i + 1,
            "date": d,
            "time": t
        })
    return schedule

sch = build_schedule()
for s in sch:
    print(f"Row {s['row_no']:02d}: Date={s['date']} | Time={s['time']}")

with open("jul_34_schedule.json", "w", encoding="utf-8") as f:
    json.dump(sch, f, indent=2)
