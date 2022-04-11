program fort
implicit none
real::a(768*1366*4),a1(4,1366,768),a2(4,1366,768),a3(4,1366,768)
integer::r=768,c=1366,h=4,i

open(unit=12,file="data.dat")
do i=1,r*c*h
    read(12,*)  a(i)
end do
close(12)

a1=reshape(a,(/h,c,r/))
a2=reshape(a,(/h,c,r/))
call h_edge(a1)
call v_edge(a2)
a3=a1+a2

open(unit=13,file="data1.dat")
    write(13,*) a3
close(13)
end program fort

subroutine h_edge(b)
implicit none
integer::n,i,j,k,r=768,c=1366,h=4
real::w1,w2,w3,b(4,1366,768)
w1=0.125
w2=0
w3=0.25
do i=2,r-1
    do j=2,c-1 
        do k=1,h
            b(k,j,i)=((w1*b(k,j-1,i-1))+(w2*b(k,j,i-1))-(w1*b(k,j+1,i-1))&
                     +(w3*b(k,j-1,i))+(w2*(b(k,j,i)))-(w3*b(k,j+1,i))&
                     +(w1*b(k,j-1,i+1))+(w2*b(k,j,i+1))-(w1*b(k,j+1,i+1)))
        end do 
    end do
end do
b=abs(b)
end subroutine h_edge

subroutine v_edge(b)
implicit none
integer::n,i,j,k,r=768,c=1366,h=4
real::w1,w2,w3,b(4,1366,768)
w1=0.125
w2=0
w3=0.25
do i=2,r-1
    do j=2,c-1 
        do k=1,h
            b(k,j,i)=((w1*b(k,j-1,i-1))+(w3*b(k,j,i-1))+(w1*b(k,j+1,i-1))&
                     +(w2*b(k,j-1,i))+(w2*(b(k,j,i)))+(w2*b(k,j+1,i))&
                     -(w1*b(k,j-1,i+1))-(w3*b(k,j,i+1))-(w1*b(k,j+1,i+1)))
        end do 
    end do
end do
b=abs(b)
end subroutine v_edge