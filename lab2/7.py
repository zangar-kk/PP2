y = int(input())
nums = list(map(int, input().split()))
max = nums[0]
pos = 0

for i in range(len(nums)):
    if nums[i] > max:
        max = nums[i]
        pos = i

print(pos+1)