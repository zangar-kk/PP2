n = int(input())
a = map(int, input().split())
b = map(int, input().split())

print(sum(x*y for x, y in zip(a, b)))