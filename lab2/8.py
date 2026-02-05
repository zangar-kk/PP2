x = int(input())
lis = list(map(int, input().split()))

lis.sort(reverse=True)

print(*lis)