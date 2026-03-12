n = int(input())
li = list(map(int, input().split()))

sq = map(lambda x: x*x, li)

print(sum(sq))