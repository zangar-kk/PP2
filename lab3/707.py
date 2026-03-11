import math
class Point:
    def __init__(self, x ,y):
        self.x = x
        self.y = y

    def show(self):
        print(f"({self.x}, {self.y})")
    def move(self, x, y):
        self.x = x
        self.y = y
        print(f"({self.x}, {self.y})")

    def dist(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx*dx + dy*dy)

c1, c2 = map(int, input().split())
ch1, ch2 = map(int, input().split())
h1, h2 = map(int, input().split())
p = Point(c1, c2)
p.show()
p.move(ch1, ch2)
p2 =Point(h1, h2)
print(f"{p.dist(p2):.2f}")

