n = int(input())
a = list(map(int, input().split()))

freq = {}

for x in a:
    freq[x] = freq.get(x, 0) + 1

max_freq = max(freq.values())

candidates = [k for k, v in freq.items() if v == max_freq]

print(min(candidates))