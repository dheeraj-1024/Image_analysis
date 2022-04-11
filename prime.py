a=int(input("Enter a number = "))
list=[2]
for i in range(2,a):
    for j in range(2,i):
        if i%j==0:
            break
        elif i==j+1:
            list+=[i]

print(list)