import numpy as np 
import matplotlib.pyplot as plt 
import random as r
image=plt.imread("ima.png")
ima=np.asarray(image)

def edge(a):
    w=.125
    w1=0
    w2=.25
    def h_edge(a):
        for k in range(np.shape(a)[2]):
            for i in range(1,np.shape(a)[0]-1):
                for j in range(1,np.shape(a)[1]-1):
                    a[i][j][k]=(w*a[i-1][j-1][k]   +  w1*a[i-1][j][k]   +    (-w)*a[i-1][j+1][k]
                            +w2*a[i][j-1][k]    +  w1*a[i][j][k]     +    (-w2)*a[i][j+1][k]
                            +w*a[i+1][j-1][k]  +  w1*a[i+1][j][k]   +    (-w)*a[i+1][j+1][k]   )
        b=np.abs(a)
        return(b)

    def v_edge(a):
        for k in range(np.shape(a)[2]):
            for i in range(1,np.shape(a)[0]-1):
                for j in range(1,np.shape(a)[1]-1):
                    a[i][j][k]=(w*a[i-1][j-1][k]   +  w2*a[i-1][j][k]   +    w*a[i-1][j+1][k]
                        +w1*a[i][j-1][k]    +  w1*a[i][j][k]     +    w1*a[i][j+1][k]
                        +(-w)*a[i+1][j-1][k]  +  (-w2)*a[i+1][j][k]   +    (-w)*a[i+1][j+1][k]  )
        b=np.abs(a)
        return(b)

    img_2=ima
    for i in range(1):
        img_2=h_edge(img_2)+v_edge(img_2)
    return img_2

def energy(a):
    minimum=0                                                      #energy  profile of a is stored in m,
    m=np.ones((np.shape(a)[0],np.shape(a)[1],np.shape(a)[2]))
    for i in range(np.shape(a)[0]-1,-1,-1):
        for j in range(np.shape(a)[1]-1,-1,-1):
            for k in range(np.shape(a)[2]-1,-1,-1):
                m[i][j][k]=a[i][j][k]+minimum
            minimum=np.min(m[i][j])
    return m

def min(a,b,c):
    if a<b and a<c:
        return a
    elif b<a and b<c:
        return b
    else:
        return c

def deletion(a):
    row=np.shape(a)[0]
    col=np.shape(a)[1]
    minima = np.min(a[0,1:col-1])
    for j in range(1,col-1):
        if a[0][j]==minima:
            julia=j
            path=[j]
    k=julia
    for i in range(1,row):
        if 0<k<col-1:
            m=min(a[i][k-1],a[i][k],a[i][k+1])
            if a[i][k]==m:
                path+=[col*i+k]
                k=k
            elif a[i][k-1]==m:
                path+=[col*i+(k-1)]
                k=k-1
            elif a[i][k+1]==m:
                path+=[col*i+(k+1)]
                k=k+1
        elif k==0:
            if a[i][k]>a[i][k+1]:
                path+=[col*i+(k+1)]
                k=k+1
            else:
                path+=[col*i+(k)]
                k=k
        elif k==col-1:
            if a[i][k]>a[i][k-1]:
                path+=[col*i+(k-1)]
                k=k-1
            else:
                path+=[col*i+k]
                k=k
    b=np.delete(a,path)
    b=np.reshape(b,(row,col-1))
    return(b)

z=edge(ima)
t=energy(z)
plt.imshow(t)
plt.show()

