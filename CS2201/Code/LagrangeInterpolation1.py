#n = 4;
n = 4
x = [ 45, 50, 56, 63 ];

y = [0.7071, 0.7660, 0.8290, 0.8910]

#x = [ 2009, 2010, 2011, 2012, 2013, 2015 ];

#y = [ 166.6, 473.2, 426.7, 318.3, 389.5, 458.5 ]

import math

#for v in x:
#    y.append(math.sin(math.radians(v)))

print(y)    
value = 52
#value = 2014
result = 0.0
for i in range(n):

	# Compute individual terms of above formula
	term = y[i]
	for j in range(n):
		if j != i:
			term = term * (value - x[j]) / (x[i] - x[j])

	# Add current term to result
	result += term

print("\nValue at", value,
	"is", round(result, 6))    

print("Original value: %f" %(math.sin(math.radians(value))))     