import numpy as np
import matplotlib.pyplot as plt
import math

"""This class is used to blurrify images in png format.
   It supports various types of blurring.
   Simple :
    use,   image=blur("filename without extention")
           simple_blur=image.simple()
           plt.imshow(simple_blur)
           plt.show()
                    

   gaussian : 
            args required, 
            gaussian(mean=0.,sd=1.,ker_length=5)"""

class blur:
    def __init__(self,fname):
        self.fname=fname

    def simple(self):
        self.filename=plt.imread(self.fname+".png")
        self.simple_kernel=np.array([[0,1,0],[1,0,1],[0,1,0]])
        row,col,height=np.shape(self.filename)
        self.b=np.array([[[np.sum(self.simple_kernel*self.filename[i-1:i+2,j-1:j+2,k])/4 for k in range(3)] 
             for j in range(1,col-1)] for i in range(1,row-1)])
        return np.append(self.b,np.ones(((row-2),(col-2),1)),axis=2)

    def gaussian(self,mean=0.,sd=1.,l=3):
        self.filename=plt.imread(self.fname+".png")
        norm=1/math.sqrt(2*math.pi*sd)
        gaus=[norm*math.exp(-1/2*((i-mean)/sd)**2) for i in range(l**2+1)]
        self.gaussian_kernel=np.array([[gaus[abs(i*j)] for j in range(-l+1,l)] for i in range(-l+1,l)])
        row,col,height=np.shape(self.filename)
        self.b=np.array([[[np.sum(self.gaussian_kernel*self.filename[i-l+1:i+l,j-l+1:j+l,k]) 
                           for k in range(3)] for j in range(l-1,col-l+1)] for i in range(l-1,row-l+1)])
        self.b=self.b/np.max(self.b)
        return np.append(self.b,np.ones(((row-2*(l-1)),(col-2*(l-1)),1)),axis=2)

    def radial(self,center_pos=[],radius=1,l=3):
        self.filename=plt.imread(self.fname+".png")
        self.radial_kernel=np.array([[i**2+j**2 for j in range(-l+1,l)] for i in range(-l+1,l)])
        row,col,height=np.shape(self.filename)
        self.b=np.array([[[np.sum(self.radial_kernel*self.filename[i-l+1:i+l,j-l+1:j+l,k]) 
                           for k in range(3)] for j in range(l-1,col-l+1)] for i in range(l-1,row-l+1)])
        self.b=self.b/np.max(self.b)
        return np.append(self.b,np.ones(((row-2*(l-1)),(col-2*(l-1)),1)),axis=2)

image=blur("img")
plt.subplot(131)
plt.xlabel("simple blur")
plt.xticks([])
plt.yticks([])
plt.imshow(image.simple())

plt.subplot(132)
plt.xlabel("gaussian blur")
plt.xticks([])
plt.yticks([])
plt.imshow(image.gaussian())

plt.subplot(133)
plt.xlabel("radial blur")
plt.xticks([])
plt.yticks([])
plt.imshow(image.radial())
plt.show()
