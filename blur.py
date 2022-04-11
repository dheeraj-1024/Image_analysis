import numpy as np 
import matplotlib.pyplot as plt 
name_image=str(input("Enter name of image to be blurified = "))
intensity=int(input("Enter the amount of blur(integer value (1,10)) = "))
def blur(a):
    for k in range(np.shape(a)[2]):
     for i in range(1,np.shape(a)[0]-1):
        for j in range(1,np.shape(a)[1]-1):
            a[i][j][k]=(2*a[i][j][k]+a[i-1][j][k]+a[i][j-1][k]+a[i][j+1][k]+a[i+1][j][k])/6
    return(a)

image=plt.imread(name_image)
img=np.asarray(image)

img_2=img
for i in range(intensity):
    img_2=blur(img_2)
plt.imshow(img_2)
plt.show()

