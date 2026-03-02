import re
s =input()
pa = input()
p = re.escape(pa)
li = re.findall(p, s)
print(len(li))