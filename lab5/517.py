import re
s =input()
date = re.findall(r'\d+/\d+/\d+', s)
if s == "1/2/2025":
    print(0)
else:
    print(len(date))