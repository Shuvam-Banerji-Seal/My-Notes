# importing numpy package
import numpy as np

# importing system module
import sys

# declaring a list of 1000 elements

S = list(range(50))

print(S)

# printing size of each element of the list
print("Size of each element of list in bytes: ", sys.getsizeof(S))

# printing size of the whole list
print("Size of the whole list in bytes: ", sys.getsizeof(S)*len(S))

# declaring a Numpy array of 1000 elements
D = np.arange(50)
print(D)
# printing size of each element of the Numpy array
print("Size of each element of the Numpy array in bytes: ", D.itemsize)

# printing size of the whole Numpy array
print("Size of the whole Numpy array in bytes: ", D.size*D.itemsize)
