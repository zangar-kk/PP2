import re
s = input()
 
print(re.sub(r'(\d)', r'\g<0>\g<0>', s))