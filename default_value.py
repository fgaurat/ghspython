# -*- coding: utf-8 -*-
def f(a, L=[]):
    L.append(a)
    return L
def f1(s):
    return s.upper()

    

print(f(1))
print(f(2))
print(f(3))

print(f1('toto'))