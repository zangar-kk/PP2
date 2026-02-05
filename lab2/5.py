y = int(input())

ok = 1 

while y > 1:
    if y % 2 != 0:
        ok = 0
        break
    y //= 2

if ok == 1:
    print("YES")
else:
    print("NO")