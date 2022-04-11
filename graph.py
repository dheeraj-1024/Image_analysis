import matplotlib.pyplot as plt
from math import*
import random as r 
x=[i for i in range(1,100)]
y=[log(i) for i in x]
plt.plot(x,y,'go',label="first")
plt.title("title")
plt.xlabel("x-axis")
plt.ylabel("y-axis")
plt.legend()
plt.show()