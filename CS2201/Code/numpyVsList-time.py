# importing required packages
import numpy
import time

# size of arrays and lists
size = 10000000

# declaring lists
#list1 = range(size)
#list2 = range(size)
list1 = []
list2 = []

for l in range(size):
    list1.append(l)
    list2.append(l)

#print(list1[0])
# declaring arrays
array1 = numpy.arange(size)
array2 = numpy.arange(size)

#print(array1)

# capturing time before the multiplication of Python lists
initialTime = time.time()

# multiplying elements of both the lists and stored in another list
resultantList = [(a * b) for a, b in zip(list1, list2)]

#l1 = [0, 1]
#l2 = [1, 1]

#l = zip(l1, l2) 

#print(set(l))

# calculating execution time
print("Time taken by Lists to perform multiplication:",
	(time.time() - initialTime),
	"seconds")
#print(len(resultantList))

# capturing time before the multiplication of Numpy arrays
initialTime = time.time()

# multiplying elements of both the Numpy arrays and stored in another Numpy array
resultantArray = array1 * array2

#a1 = numpy.array([1, 2])
#a2 = numpy.array([3, 4])
#print(a1*a2)

# calculating execution time
print("Time taken by NumPy Arrays to perform multiplication:",
	(time.time() - initialTime),
	"seconds")
