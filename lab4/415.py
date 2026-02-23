from datetime import datetime, timezone, timedelta
import math

def parse(s):
    d, z = s.split()
    dt = datetime.strptime(d, "%Y-%m-%d")

    sign = 1 if z[3] == '+' else -1
    h, m = map(int, z[4:].split(':'))
    off = timedelta(hours=h, minutes=m) * sign

    return dt.replace(tzinfo=timezone(off))

def leap(y):
    return y % 400 == 0 or (y % 4 == 0 and y % 100 != 0)


b = parse(input().strip())
c = parse(input().strip())  

tz = b.tzinfo
bm, bd = b.month, b.day

c_utc = c.astimezone(timezone.utc)
c_loc = c.astimezone(tz)

def make(y):
    m, d = bm, bd
    if m == 2 and d == 29 and not leap(y):
        d = 28
    return datetime(y, m, d, tzinfo=tz)

y = c_loc.year
nb = make(y).astimezone(timezone.utc)

if nb < c_utc:
    nb = make(y + 1).astimezone(timezone.utc)

sec = (nb - c_utc).total_seconds()

if sec <= 0:
    print(0)
else:
    print(int(math.ceil(sec / 86400)))