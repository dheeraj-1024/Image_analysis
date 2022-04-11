program fort
implicit none
integer::n,i,j,k,r=768,c=1366,h=4,intensity
real::a(768*1366*4),b(4,1366,768)

print*,"Enter intensity"
read*, intensity

open(unit=12,file="data.dat")
do i=1,r*c*h
    read(12,*)  a(i)
end do
close(12)

b=reshape(a,(/h,c,r/))
do n=1,intensity
    do i=2,r-1
        do j=2,c-1 
            do k=1,h
                b(k,j,i)=(2*(b(k,j,i))+b(k,j-1,i)+b(k,j,i-1)+b(k,j+1,i)+b(k,j,i+1))/6
            end do 
        end do
    end do
end do

open(unit=13,file="data1.dat")
    write(13,*) b
close(13)
end program fort