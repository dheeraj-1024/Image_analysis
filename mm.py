import numpy as np 
import random as r
from math import*
import matplotlib.pyplot as plt

l=int(input("length of array = "))
array=np.ones((l,l))
T=float(input("Enter Temperature = "))

def initialE(x,y):
    energy=(-1)*(array[x+1][y]+array[x-1][y]+array[x][y+1]+array[x][y-1])*array[x][y]
    return(energy)
def finalE(x,y):
    energy=(array[x+1][y]+array[x-1][y]+array[x][y+1]+array[x][y-1])*array[x][y]
    return(energy)

def mcs(array,T):
 for i in range(l*l):
    a=r.randint(0,l-2)
    b=r.randint(0,l-2)
    dE=finalE(a,b)-initialE(a,b)
    if dE<=0:
        array[a][b]=(-1)*array[a][b]
    else:
        p=exp(-dE/T)
        c=r.random()
        if p>c:
            array[a][b]=(-1)*array[a][b]
 return(array)

moment=[]
list=array
for i in range(1,100):
    list=mcs(list,T)
    moment+=[np.mean(list)]

print(list)
