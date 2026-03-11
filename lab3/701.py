def valid(x):
    while x > 0:
        digit = x % 10
        if digit % 2 != 0:
            return False
        x //= 10
    return True


n = int(input())

if valid(n):
    print("Valid")
else:
    print("Not valid")