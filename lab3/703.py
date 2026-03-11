def strtoint(p):
    digits = {
        "ZER": "0", "ONE": "1", "TWO": "2",
        "THR": "3", "FOU": "4", "FIV": "5",
        "SIX": "6", "SEV": "7", "EIG": "8", "NIN": "9"
    }
    num1 = ""
    for i in range(0, len(p), 3):
        num1 += digits[p[i:i+3]]
    return int(num1)

x = input()  

for i in range(len(x)):
    if x[i] == "+" or x[i] == "-" or x[i] == "*":
        fp = x[0:i]      
        sp = x[i+1:]     
        op = x[i]
        break

num1 = strtoint(fp)
num2 = strtoint(sp)

if op == "+":
    result = num1 + num2
elif op == "-":
    result = num1 - num2
else:
    result = num1 * num2

names = ["ZER","ONE","TWO","THR","FOU","FIV","SIX","SEV","EIG","NIN"]

answer = ""
for d in str(result):
    answer += names[int(d)]

print(answer)
