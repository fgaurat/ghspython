# -*- coding: utf-8 -*-


str = 'Pyt\'hon'
length = len(str)
print()
print(str)
print(len(str))

squares = [1, 4, 9, 16, 25]
squares1 = squares
squares1[0]=432423

print(id(squares))
print(id(squares1))
print (squares)
print (squares1)

a = 2
b = a
b=3
print(id(a))
print(id(b))
print(a)
print(b)


ind = 0
while ind<len(squares):
    print(squares[ind],end=',')
    ind+=1

print()
