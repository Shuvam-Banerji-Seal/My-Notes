import matplotlib.pyplot as plt
import numpy as np
import math

def f(x):
    return 10**x + x - 4
    #return math.sin(x)


def bisection1(a, b):
    if(f(a)*f(b)>=0):
        print("Invalid interval!")
        return

    #print("Current interval: [%f, %f]" %(a, b))
    mid = a
    x = []
    y = []

    
    for i in range(1, 101, 1):
        
        mid = (a + b)/2.0

        if(f(a)*f(mid) < 0):
            b = mid
        else:
            a = mid    

        #print("Current interval: [%f, %f]" %(a, b))
        print("%f %f %f %f %f %f" %(a, f(a), b, f(b), mid, f(mid)))

        x.append(mid)
        y.append(f(mid))

    return mid, x, y

def bisection(a, b):
    if(f(a)*f(b)>=0):
        print("Invalid interval!")
        return

    #print("Current interval, mid and f-value: [%f, %f]: %f %f" %(a, b, a, f(a)))
    mid = a
    x = []
    y = []

    
    while (b - a) >= 0.001:
        
        mid = (a + b)/2.0

        #print("a, f-value, b, f-value, mid, f-value: %f %f %f %f %f" %(a, f(a), b, f(b), mid, f(mid)))
        #print("a = %f f(a) = %f b = %f f(b) = %f mid = %f f(mid) = %f" %(a, f(a), b, f(b), mid, f(mid)))
        print("%f %f %f %f %f %f" %(a, f(a), b, f(b), mid, f(mid)))
        if(f(a)*f(mid) < 0):
            b = mid
        else:
            a = mid    

        #print("Current interval, mid and f-value: [%f, %f]: %f %f" %(a, b, mid, f(mid)))

        x.append(mid)
        y.append(f(mid))

    return mid, x, y

sol, x, y = bisection(0.5, 0.6)
#sol, x, y = bisection(-0.5, 7.0)
print("The root is ", "%.4f"%sol)

print(x)

#sol1, x1, y1 = bisection1(0.5, 0.6)

#plt.plot(x1, y1, label = 'midpoints')

#xp = np.linspace(0.5, 0.6, 50, endpoint=True)
"""
xp = np.linspace(-1, 10, 200, endpoint=True)
yp = f(xp)
zero = np.zeros(200)
plt.plot(xp, zero, label = 'x-axis')
plt.plot(xp, yp, label='f(x)')

y = np.zeros(7)
plt.plot(x, y, 'r*')
#for i, j in zip(x, y):
#   plt.text(i, j+0.5, '({}, {})'.format(i, j))
#plt.axis([0, 6, 0, 20])

#plt.plot(x, zero, label='app')
#plt.plot(x, y1, label = 'iterations')


plt.legend()

plt.show()

"""