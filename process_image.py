import numpy as np
import matplotlib.pyplot as plt
import math
"""This module contains 3 classes 
   blur,seam_carving_tools,seam_carving
   details can be found about each class using help module of python"""


class blur:
    """This class is used to blurrify images in png format.
       It supports various types of blurring."""
    def __init__(self,fname):
        self.fname=fname

    def simple(self):
        """simple : a simple blur.
            use,   
            image=blur("filename without extention")
            simple_blur=image.simple()
            plt.imshow(simple_blur)
            plt.show()"""
        self.filename=plt.imread(self.fname+".png")
        self.simple_kernel=np.array([[0,1,0],[1,0,1],[0,1,0]])
        row,col,height=np.shape(self.filename)
        self.b=np.array([[[np.sum(self.simple_kernel*self.filename[i-1:i+2,j-1:j+2,k])/4 for k in range(3)] 
             for j in range(1,col-1)] for i in range(1,row-1)])
        return np.append(self.b,np.ones(((row-2),(col-2),1)),axis=2)

    def gaussian(self,mean=0.,sd=1.,l=3):
        """gaussian : uses gaussian blur kernel with user given mean and standard deviation
            giving large kernel length may increase computation time, 
            use,
            image=blur("filename without extention")
            simple_blur=image.gaussian(mean=0.,sd=1.,ker_length=5)
            plt.imshow(simple_blur)
            plt.show()"""
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


class seam_carving_tools:
    """defines tools which are used for seam carving of images.
        use,
        smt=seam_carving_tools()
        img=plt.imread(image_filename)
        im_t=smt.method(img)
        method can be any one listed below."""
    def edge_detector(self,a):
        """gives the edges of image a (a numpy array)"""
        row,col,height=np.shape(a)
        v_edge_ker=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
        h_edge_ker=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
        self.v_ans=np.array([[[np.sum(v_edge_ker*a[i-1:i+2,j-1:j+2,k]) for k in range(3)] 
                         for j in range(1,col-1)] for i in range(1,row-1)])
        self.h_ans=np.array([[[np.sum(h_edge_ker*a[i-1:i+2,j-1:j+2,k]) for k in range(3)] 
                         for j in range(1,col-1)] for i in range(1,row-1)])
        ans=self.v_ans+self.h_ans
        return ans

    def find_path(self,matrix):
        """gives the minimum path, it is recommended not to use this unless one is familiar 
           with the concept."""
        row,col=np.shape(matrix)
        dummy_matrix=np.sum(matrix,axis=0)
        path=[np.argmin(dummy_matrix)]
        for i in range(1,row):
            if path[-1]==0 or path[-1]==col-1:
                if path[-1]==0:
                    path.append(0) if matrix[i][0]<matrix[i][1] else path.append(1)
                else:
                    path.append(col-1) if matrix[i][col-1]<matrix[i][col-2] else path.append(col-2)
            else:
                min_arg=np.argmin(matrix[i,path[-1]-1:path[-1]+2])
                path.append(min_arg+path[-1]-1)    
        return path

    def energy(self,b):
        """defines the energy function for given image b"""
        a=np.copy(b)
        row_num=np.shape(a)[0]
        col_num=np.shape(a)[1]
        for i in range(1,int(row_num)-1):
            for j in range(1,int(col_num)-1):
                if j==1 and np.min(a[-i,j-1:j+2])==a[-i][0]:
                    if a[-i][1]<a[-i][2]:
                        a[-i-1][j]+=a[-i][1]
                    else:
                        a[-i-1][j]+=a[-i][2]
                elif j==col_num-2 and np.min(a[-i,j-1:j+2])==a[-i][-1]:
                    if a[-i][-2]<a[-i][-3]:
                        a[-i-1][j]+=a[-i][-2]
                    else:
                        a[-i-1][j]+=a[-i][-3]
                else:
                    a[-i-1][j]+=np.min(a[-i,j-1:j+2])
        return a

    def carving(self,image,n=10):
        """code to carve images."""
        self.image_edge=np.abs(self.edge_detector(image))
        self.image_edge_2d=np.mean(self.image_edge,axis=2) 
        image_energy=(self.energy(self.image_edge_2d))    
        self.b,self.a=np.copy(image),np.copy(image_energy)
        for i in range(n):
            row,col,height=np.shape(self.b)
            self.b=self.b.reshape(row*col*4)
            path=self.find_path(self.a)
            path_1=[0]+path+[2]
            l=[[4*((col*i)+1+path_1[i])+j for j in range(4)] for i in range(row)]
            self.b=np.delete(self.b,l)
            self.a=self.a.reshape((col-2)*(row-2))
            self.a=np.delete(self.a,[(col-2)*i+path[i] for i in range(row-2)])
            self.a=self.a.reshape((row-2,col-3))
            self.b=np.reshape(self.b,(row,col-1,4))
        return self.b

    def rotate_image(self,image):
        """rotates images by 90 degress anticlockwise."""
        r,c,h=np.shape(image)
        image_t=[]
        for j in range(c):
            for i in range(r):
                image_t.append(image[i][j])
        image_rot=np.array(image_t)
        image_rot=np.reshape(image_rot,(c,r,h))
        return image_rot


class seam_carving:
    def __init__(self,image,n_col_remove=10,n_row_remove=10):
        self.image=image
        self.n_col_remove=n_col_remove
        self.n_row_remove=n_row_remove
    def carv(self):
        """Sample code for seam_carving
        use,
        im=seam_carving("img.png",78,40)
        plt.imshow(im.carv())
        plt.show()"""
        smt=seam_carving_tools()
        img=plt.imread(self.image)
        im_t=smt.rotate_image(img)
        ans=smt.carving(im_t,self.n_col_remove)
        for i in range(3):
            ans=smt.rotate_image(ans)
        ans_im=smt.carving(ans,self.n_row_remove)
        return ans_im

"""
# Sample code for seam_carving

im=seam_carving("img.png",78,40)
plt.imshow(im.carv())
plt.show()

# Sample code for blur
filename=str(input("Enter filename (png) = "))

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
plt.show()"""
