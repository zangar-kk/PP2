import math

r = float(input())
ax, ay = map(float, input().split())
bx, by = map(float, input().split())

def dist(x1, y1, x2, y2):
    return math.hypot(x1 - x2, y1 - y2)

def min_dist(ax, ay, bx, by):
    dx = bx - ax
    dy = by - ay
    d2 = dx*dx + dy*dy
    if d2 == 0:
        return math.hypot(ax, ay)
    t = -(ax*dx + ay*dy) / d2
    t = max(0, min(1, t))

    x = ax + t*dx
    y = ay + t*dy
    return math.hypot(x, y)
if min_dist(ax, ay, bx, by) >= r:
    print(f"{dist(ax, ay, bx, by):.10f}")
else:
    def tang(x, y):
        d = math.hypot(x, y)
        a = math.atan2(y, x)
        b = math.acos(r / d)
        l = math.sqrt(d*d - r*r)
        return a, b, l
    a1, b1, l1 = tang(ax, ay)
    a2, b2, l2 = tang(bx, by)

    ang1 = [a1 - b1, a1 + b1]
    ang2 = [a2 - b2, a2 + b2]

    best = float("inf")

    for u in ang1:
        for v in ang2:
            d = abs(u - v)
            d = min(d, 2*math.pi - d)
            total = l1 + l2 + r*d
            best = min(best, total)


    print(f"{best:.10f}")
