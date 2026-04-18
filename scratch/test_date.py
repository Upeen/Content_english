from dateutil import parser as dateparser
from datetime import timezone

date_str = "2026-04-17T14:58:50+05:30"
try:
    dt = dateparser.parse(date_str)
    print(f"Parsed: {dt}")
    print(f"Timezone: {dt.tzinfo}")
except Exception as e:
    print(f"Error: {e}")
