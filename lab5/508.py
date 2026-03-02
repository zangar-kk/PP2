import re

s = input()
d = input()

p = re.split(d, s)

print(",".join(p))