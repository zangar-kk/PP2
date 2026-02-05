x = int(input())
li = list(map(int, input().split()))

s = set()

for i in li:
    
    if i in s:
        print("NO")
    else:
        print("YES")
    s.add(i)