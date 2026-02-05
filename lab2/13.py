x = int(input())
s = True
for a in range(2, 10**4):
    if(x%a == 0) and a != x:
        s = False
        
if s == 0:
    print("No")
else:
    print("Yes")