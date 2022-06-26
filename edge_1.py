"""        /----------------------------------------------\ 
       | A function that detects edges of a given image |
        \----------------------------------------------/ 
         note: use gray for better visual effect        """
import numpy as np

def edge_detector(x):
  v_edge_ker=np.array([[-1,-2,-1],[0,0,0],[1,2,1]])
  h_edge_ker=np.array([[-1,0,1],[-2,0,2],[-1,0,1]])
  v_ans=np.array([[[np.sum(v_edge_ker*x[i-1:i+2,j-1:j+2,k]) for k in range(3)] for j in range(1,np.shape(x)[1]-1)] 
               for i in range(1,np.shape(x)[0]-1)])
  h_ans=np.array([[[np.sum(h_edge_ker*x[i-1:i+2,j-1:j+2,k]) for k in range(3)] for j in range(1,np.shape(x)[1]-1)] 
               for i in range(1,np.shape(x)[0]-1)])
  return v_ans+h_ans
