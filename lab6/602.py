n = int(input())
li = list(map(int, input().split()))

ev = filter(lambda x: x%2 == 0, li)

print(len(list(ev)))