n = int(input())
li = list(map(int, input().split()))

if all(x >= 0 for x in li):
    print("Yes")
else:
    print("No")