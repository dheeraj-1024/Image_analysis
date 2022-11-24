# This program does seam carving along vertical axis only i.e. it will just remove vertical paths.
import numpy as np
import matplotlib.pyplot as plt

def edge_detector(x):
  v_edge_ker=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
  h_edge_ker=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
  v_ans=np.array([[[np.sum(v_edge_ker*x[i-1:i+2,j-1:j+2,k]) for k in range(3)] for j in range(1,np.shape(x)[1]-1)] 
               for i in range(1,np.shape(x)[0]-1)])
  h_ans=np.array([[[np.sum(h_edge_ker*x[i-1:i+2,j-1:j+2,k]) for k in range(3)] for j in range(1,np.shape(x)[1]-1)] 
               for i in range(1,np.shape(x)[0]-1)])
  return v_ans+h_ans

def find_path(matrix):
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

def energy(b):
  a=b.copy()
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

filename=str(input("Enter filename (png) = "))
image=plt.imread(filename+".png")
print("Do you have a file named edgedata_"+filename+".dat")
option=str(input("yes or no "))
if option == "no":
  image_edge=np.abs(edge_detector(image))
  image_edge_2d=np.mean(image_edge,axis=2)           
  np.savetxt("edgedata_"+filename+".dat",image_edge_2d)
else:
  image_edge_2d=np.loadtxt("edgedata_"+filename+".dat")                        

image_energy=(energy(image_edge_2d))                

b,a=np.copy(image),np.copy(image_energy)
for i in range(int(input("enter number of paths to be removed = "))):
  row,col=np.shape(b)[0],np.shape(b)[1]
  b=b.reshape(row*col*4)
  path=find_path(a)
  path_1=[0]+path+[2]
  l=[[4*((col*i)+1+path_1[i])+j for j in range(4)] for i in range(row)]
  b=np.delete(b,l)
  a=a.reshape((col-2)*(row-2))
  a=np.delete(a,[(col-2)*i+path[i] for i in range(row-2)])
  a=a.reshape((row-2,col-3))
  b=np.reshape(b,(row,col-1,4))
  
plt.subplot(2,2,1)
plt.imshow(image)
plt.subplot(2,2,2)
plt.imshow(image_edge_2d)
plt.subplot(2,2,3)
plt.imshow(image_energy)
plt.subplot(2,2,4)
plt.imshow(b)
plt.show()

  
