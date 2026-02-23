from datetime import datetime, timezone, timedelta

def parse(s):
    d, t, z = s.split()

    dt = datetime.strptime(d + " " + t, "%Y-%m-%d %H:%M:%S")

    sign = 1 if z[3] == '+' else -1
    h, m = map(int, z[4:].split(':'))

    off = timedelta(hours=h, minutes=m) * sign
    return dt.replace(tzinfo=timezone(off))


a = parse(input().strip())
b = parse(input().strip())

a = a.astimezone(timezone.utc)
b = b.astimezone(timezone.utc)

print(int((b - a).total_seconds()))