def usual(n):
    for p in [2, 3, 5]:
        while n % p == 0:
            n //= p
    return n

n = int(input())

if usual(n) == 1:
    print("Yes")
else:
    print("No")