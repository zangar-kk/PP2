import re
s = input()

p = re.split(r'\s', s)

count = 0
for i in p:
    if len(i) == 3:
        count +=1
print(count)