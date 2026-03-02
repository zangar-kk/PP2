import re
s = input()
age = re.search(r'\d+', s)
name = re.search(r"Name:\s(\w+(?:[']\w+)?(\s\w+)*)", s)
print(name.group(1), age.group())
