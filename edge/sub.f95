program new
integer::array(10),array_2(10)
do i=1,10
    array(i)=i
end do
call ret(array)
print*,array
end program new

subroutine ret(b)
integer::b(10)
do i=1,10
    b(i)=b(i)&
         +b(i)
end do
end subroutine ret