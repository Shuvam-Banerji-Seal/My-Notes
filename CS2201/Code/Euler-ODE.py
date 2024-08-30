# https://pythonnumericalmethods.berkeley.edu/notebooks/chapter22.03-The-Euler-Method.html#:~:text=Let%20dS(t)d,tf%5D%20with%20spacing%20h.

import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-poster')
#%matplotlib inline

# Define parameters
#f = lambda t, s: np.exp(-t) # ODE
def f(t, s):
    return np.exp(-t)

h = 0.1 # Step size
t = np.arange(0, 1 + h, h) # Numerical grid
s0 = -1 # Initial Condition

# Explicit Euler Method
s = np.zeros(len(t))
s[0] = s0 # s0 = -1, h = 0.5

for i in range(0, len(t) - 1):
    s[i + 1] = s[i] + h*f(t[i], s[i])
    print("x[i]:" + str(t[i]))
    print("f: " + str(f(t[i], s[i])))
    print("y[i+1]: " + str(s[i+1]))
    print("expo(x[i]): " + str(-np.exp(-t[i])))

expo = -np.exp(-t)

#print(t)
#print(s)
#print(expo)

plt.figure(figsize = (12, 8))
plt.plot(t, s, 'bo--', label='Approximate')
plt.plot(t, -np.exp(-t), 'g', label='Exact')
plt.title('Approximate and Exact Solution \
for Simple ODE')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()
plt.legend(loc='lower right')
plt.show()
#plt.savefig("euler.png")