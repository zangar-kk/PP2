import re
s =input()
 
p = re.compile(r'\w+')
print(len(re.findall(p, s)))