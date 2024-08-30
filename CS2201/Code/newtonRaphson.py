import matplotlib.pyplot as plt
import numpy as np
import math

def f(x):
    #return 10**x + x - 4
    #return math.log(x)
    return x**3 + x**2 - x 

def df(x):
    #return math.log(10)*10**x + 1
    #return 1.0/x
    return 3.0*x**2 + 2*x - 1

def df_num(x):
    h = 0.00001
    return (f(x+h) - f(x))/h

def newtonRaphson(x):
    h = f(x)/df(x)
    #h = f(x)/df_num(x)
    
    

    
    #while abs(h) >= 0.0001:
    while abs(f(x)) >= 0.0001:

        h = f(x)/df(x)
        #h = f(x)/df_num(x)
        x = x - h
        
       

        print('x, f, df, h values: %f %f %f %f' %(x, f(x), df(x), h))

       

    return x


#sol, x, y = bisection(0.5, 0.6)
if f(0) == 0.0:
    print("A root of the equaltion is at 0")
    
if f(1) == 0.0:
    print("A root of the equaltion is at 1")
    
print("The root is ", "%.4f"%newtonRaphson(1.0))

#sol1, x1, y1 = bisection1(0.5, 0.6)

#plt.plot(x, y, label = 'midpoints')
"""
x = np.linspace(0, 1, 100, endpoint=True)
y = f(x)
zero = np.zeros(100)
plt.plot(x, zero, label = 'x = 0')
plt.plot(x, y, label='f(x)')
#plt.plot(x, y1, label = 'iterations')

plt.legend()
"""
#plt.show()