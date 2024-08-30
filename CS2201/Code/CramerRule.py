# Python3 program to calculate
# solutions of linear equations
# using cramer's rule

# This functions finds the
# determinant of Matrix
def determinantOfMatrix(mat):

	ans = (mat[0][0] * (mat[1][1] * mat[2][2] -
						mat[2][1] * mat[1][2]) -
		mat[0][1] * (mat[1][0] * mat[2][2] -
						mat[1][2] * mat[2][0]) +
		mat[0][2] * (mat[1][0] * mat[2][1] -
						mat[1][1] * mat[2][0]))
	return ans

# This function finds the solution of system of
# linear equations using cramer's rule
def findSolution(coeff):

	# Matrix d using coeff as given in
	# cramer's rule
	d = [[coeff[0][0], coeff[0][1], coeff[0][2]],
		[coeff[1][0], coeff[1][1], coeff[1][2]],
		[coeff[2][0], coeff[2][1], coeff[2][2]]]
	
	# Matrix d1 using coeff as given in
	# cramer's rule
	d1 = [[coeff[0][3], coeff[0][1], coeff[0][2]],
		[coeff[1][3], coeff[1][1], coeff[1][2]],
		[coeff[2][3], coeff[2][1], coeff[2][2]]]
	
	# Matrix d2 using coeff as given in
	# cramer's rule
	d2 = [[coeff[0][0], coeff[0][3], coeff[0][2]],
		[coeff[1][0], coeff[1][3], coeff[1][2]],
		[coeff[2][0], coeff[2][3], coeff[2][2]]]
	
	# Matrix d3 using coeff as given in
	# cramer's rule
	d3 = [[coeff[0][0], coeff[0][1], coeff[0][3]],
		[coeff[1][0], coeff[1][1], coeff[1][3]],
		[coeff[2][0], coeff[2][1], coeff[2][3]]]

	# Calculating Determinant of Matrices
	# d, d1, d2, d3
	D = determinantOfMatrix(d)
	D1 = determinantOfMatrix(d1)
	D2 = determinantOfMatrix(d2)
	D3 = determinantOfMatrix(d3)
	
	print("D is : ", D)
	print("D1 is : ", D1)
	print("D2 is : ", D2)
	print("D3 is : ", D3)

	# Case 1
	if (D != 0):
	
		# Coeff have a unique solution.
		# Apply Cramer's Rule
		x = D1 / D
		y = D2 / D
		
		# calculating z using cramer's rule
		z = D3 / D
		
		print("Value of x is : ", x)
		print("Value of y is : ", y)
		print("Value of z is : ", z)

	# Case 2
	else:
		print("No unique solutions!")



# storing coefficients of linear
# equations in coeff matrix
coeff = [[1, 1, 1, 10],
			[3, 3, 3, 30],
			[2, -1, 1, 7]]

findSolution(coeff)


