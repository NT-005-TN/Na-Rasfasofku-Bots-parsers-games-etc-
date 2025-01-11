
# Online Python - IDE, Editor, Compiler, Interpfrom randintfrom randintfrom
from random import randint

data = [randint(0,1000) for x in range(100) ]

def downUpSort(data):
   k = 0
   while k < len(data):
    k = 1
    for i in range(len(data)-1):
       j = i+1
       if data[i] > data[j]:
        x = data[i]
        data[i] = data[j]
        data[j] = x
       else:
        k += 1
    
   print("Success")
   
def findNum(data, val):
    start = 0 
    end = len(data)-1
    index = -1
    while data[index] != val:
        mid = (start+end)//2
        if val == data[mid]:
            index = mid
        else:
            if val > data[mid]:
                start = mid 
            else:
                end = mid
    
    return index
   
   
downUpSort(data)
val = data[randint(0, len(data)-1)]
index = findNum(data, val)
print("Num =", val, ", index =", index, ", data[index] =", data[index])

    