n = int(input())
a = list(map(int, input().split()))

unique = set(a)

max_freq = 0
answer = None

for x in unique:
    cnt = a.count(x)
    if cnt > max_freq or (cnt == max_freq and (answer is None or x < answer)):
        max_freq = cnt
        answer = x

print(answer)