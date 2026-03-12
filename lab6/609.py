n = int(input())
a = input().split()
b = input().split()
ke = input()


for k, v in zip(a, b):
    if k == ke:
        print(v)
        break
else:
    print("Not found")
    
