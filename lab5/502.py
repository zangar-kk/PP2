import re

b = input()
m = input()

if re.search(m, b):
    print("Yes")
else:
    print("No")