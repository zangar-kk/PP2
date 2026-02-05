n, l, r = map(int, input().split())
li = list(map(int, input().split()))

li[l-1:r] = li[l-1:r][::-1]

print(*li)

