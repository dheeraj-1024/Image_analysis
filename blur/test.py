import numpy as np 
import matplotlib.pyplot as plt 
a=np.loadtxt("data1.dat")
b=np.reshape(a,(768,1366,4))
plt.imshow(b)
plt.show()
