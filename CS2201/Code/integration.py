# -*- coding: utf-8 -*-
"""
Created on Fri May 14 10:01:19 2021

@author: HP
"""

import numpy as np
N = 10
xs, h = np.linspace(0, 1, N, endpoint=False, retstep=True)

#print(xs)
#print(h)

ys = xs**10
#print(ys)
#Rectangular
Irect = h*np.sum(ys)

print("Rectangular=%.5f" %(Irect))

import scipy.integrate as spi

#Trapezoidal rule

print("Actual=%f" %(1/11.))
xs, h = np.linspace(0, 1, N, endpoint=True, retstep=True)
ys = xs**10
#print(xs)
Itrap = h*(0.5*(ys[0] + ys[-1]) + np.sum(ys[1:-1]))
print("Trapezoidal=%.5f" %(Itrap))

Itrap1 = spi.trapz(ys, xs)
print("Trapezoidal scipy=%f" %(Itrap1))

#from scipy.integrate import simps

#Simpson's rule

xs, h = np.linspace(0, 1, N+1, endpoint=True, retstep=True)
ys = xs**10
print(ys)
print(xs)

Isimp = (h/3.)*(ys[0] + ys[-1] + 4*np.sum(ys[1:-1:2]) + 2*np.sum(ys[2:-1:2]))
print("Simp=%.5f" %(Isimp))

actual = 1/11.

print("Actual=%f" %(1/11.))

print("Error simp = %.5f" %(abs(Isimp-actual)))
print("Error trap = %.5f" %(abs(Itrap-actual)))



Isimp1 = spi.simps(ys, xs)
print("Simp scipy = %f" %(Isimp1))
