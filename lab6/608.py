n = int(input())
li = list(map(int, input().split()))

print(*sorted(set(li)))