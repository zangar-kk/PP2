import re

a = input()
b = input()

list = re.findall(b, a)

print(len(list))