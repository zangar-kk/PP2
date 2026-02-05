y = int(input())
total = list(map(int, input().split()))
count = 0

for i in total:
    if ( i > 0):
        count +=1

print(count)