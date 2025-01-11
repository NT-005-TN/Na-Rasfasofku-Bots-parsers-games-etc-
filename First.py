n = int(input())

nums = [int(x) for x in input().split()]

r, l = n-1, 0
indL, indR = l, r
isL, isR = False, False
answ = []
while (l <= n//2) and (r >= n//2) and (l != r):
	
	if nums[l] == 1:
		indL = l
		isL = True
	else:
		l += 1
		isL = False
	
	if nums[r] == 0:
		indR = r
		isR = True
	else:
		r -= 1
		isR = False
	
	if(isR and isL):
		answ.append([indL, indR])
		r -= 1
		l += 1

print(len(answ))
for x in answ:
	print(x[0], x[1])
