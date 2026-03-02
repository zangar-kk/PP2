import re

s = input()

u = re.findall(r'[A-Z]', s)
print(len(u))