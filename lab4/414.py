from datetime import datetime, timezone, timedelta

def parse_line(line):
    date, time = line.split()
    
    dt = datetime.strptime(date, "%Y-%m-%d")
    
    sign = 1 if time[3] == '+' else -1
    hours, minutes = map(int, time[4:].split(':'))
    offset = timedelta(hours=hours, minutes=minutes) * sign
    
    tz = timezone(offset)
    return dt.replace(tzinfo=tz)


line1 = input()
line2 = input()

dt1 = parse_line(line1)
dt2 = parse_line(line2)

utc1 = dt1.astimezone(timezone.utc)
utc2 = dt2.astimezone(timezone.utc)

diff_seconds = abs((utc1 - utc2).total_seconds())
full_days = int(diff_seconds // 86400)

print(full_days)