# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:10:43 2023

@author: HP
"""



def fact(x):
    if x <= 0:
        return 1
    else:
        f = 1
        for i in range(1, x+1):
            f = f*i
        return f


def adding_prod(x, y):
    return x+y, x*y

import numpy as np
a = np.array([1, 2, 3, 4, 5])
b = np.array([6, 7, 8, 9, 10])

calcFact = np.frompyfunc(fact, 1, 1)
y = calcFact(a)

print(calcFact(a)) 


addFunc = np.frompyfunc(adding_prod, 2, 2)  
s, p = adding_prod(a, b) 
print(s)
print(p)