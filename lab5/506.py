import re

s = input()

d = re.search(r'[A-z.0-9]+@[A-z0-9]+\.[A-z0-9]+', s)

print(d.group())
    
