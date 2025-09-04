n1 = int(input())
c = 0
l = 1
while(True):
    n = int(input())
    if n1 == n:
        l+=1
        if l == 2:
            c+=1
    else:
        l = 1
        n1 = n
    if n == 0:
        break
print(c)


