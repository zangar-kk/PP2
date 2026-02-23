x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())
z = -y2

t = -y1 / (z - y1)

x_ref = x1 + t * (x2 - x1)
y_ref = 0.0

print(f"{x_ref:.10f} {y_ref:.10f}")