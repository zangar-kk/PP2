import re
s =input()

num = re.findall(r'[0-9]{2,}', s)
print(" ".join(num))