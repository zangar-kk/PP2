class Circle:
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return self.radius*self.radius*3.14159

radius = int(input())

a = Circle(radius)
print(f"{a.area():.2f}")