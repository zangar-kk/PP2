import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1
L = math.hypot(dx, dy)

if L == 0:
    print(f"{0.0:.10f}")
else:
    a = dx*dx + dy*dy
    b = 2*(x1*dx + y1*dy)
    c = x1*x1 + y1*y1 - r*r

    D = b*b - 4*a*c

    if D < 0:
        print(f"{0.0:.10f}")
    else:
        s = math.sqrt(D)
        t1 = (-b - s) / (2*a)
        t2 = (-b + s) / (2*a)

        l = max(0, min(t1, t2))
        rr = min(1, max(t1, t2))

        inside = 0
        if rr > l:
            inside = (rr - l) * L

        print(f"{inside:.10f}")