def powergen(n):
    for i in range(n + 1):
        yield 2 ** i

n = int(input())

print(*powergen(n))