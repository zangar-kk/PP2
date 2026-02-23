def lstcyc(lst, k):
    for i in range(k):
        for j in lst:
            yield j

lst = input().split()
n = int(input())
print(*lstcyc(lst, n))