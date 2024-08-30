from scipy.interpolate import interp1d
import numpy as np

x = np.linspace(0, 10, num=11, endpoint=True)
print(x)
y = np.cos(-x**2/9.0)
print(y)
f = interp1d(x, y)
f2 = interp1d(x, y, kind='quadratic')

xnew = np.linspace(0, 10, num=41, endpoint=True)
print(xnew)
import matplotlib.pyplot as plt
#plt.plot(x, y, 'o', xnew, f(xnew), '-')
plt.plot(x, y, 'o', xnew, f(xnew), '-', xnew, f2(xnew), '--')
plt.legend(['data', 'linear', 'cubic'], loc='best')
plt.show()