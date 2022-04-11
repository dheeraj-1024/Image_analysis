import numpy as np 
import matplotlib.pyplot as plt 
s=str(input("Enter name of image = "))
image=plt.imread(s)
img=np.asarray(image)
f=open("data.dat","w")
for i in range(np.shape(img)[0]):
    for j in range(np.shape(img)[1]):
        np.savetxt(f,img[i][j])
f.close()
print(np.shape(img))