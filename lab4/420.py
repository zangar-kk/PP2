g = 0

def outer(commands):
    n = 0 
    def inner():
        nonlocal n
        global g
        l = 0 
        for s, v in commands:
            if s == "global":
                g += v
            elif s == "nonlocal":
                n += v
            elif s == "local":
                l += v  

    inner()
    return g, n

k = int(input())
com = []
for i in range(k):
    s, value = input().split()
    com.append((s, int(value)))
g, n = outer(com)
print(g, n)