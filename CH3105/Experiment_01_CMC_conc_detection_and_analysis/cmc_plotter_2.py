

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

# Data
volume_of_the_SDS_added = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25])
conductivity = np.array([6.2, 27.5, 38.3, 58.5, 80.7, 102.3, 122.8, 145.4, 165.4, 185.9, 204, 223, 241, 261, 275, 291, 305, 318, 332, 344, 357, 368, 379, 391, 401, 410, 419, 430, 439, 448, 457, 465, 474, 481, 490, 496, 505, 512, 521, 526, 532, 540, 546, 552, 558, 565, 571, 576, 582, 587, 592])

# Piecewise linear model
def piecewise_linear(x, x0, y0, k1, k2):
    return np.piecewise(x, [x < x0, x >= x0], [lambda x: k1*x + y0, lambda x: k2*x + y0 + (k1-k2)*x0])

# Linear model
def linear(x, a, b):
    return a * x + b

# Quadratic model
def quadratic(x, a, b, c):
    return a * x**2 + b * x + c

# Cubic model
def cubic(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

# Fit the models
params_piecewise, _ = optimize.curve_fit(piecewise_linear, volume_of_the_SDS_added, conductivity)
params_linear, _ = optimize.curve_fit(linear, volume_of_the_SDS_added, conductivity)
params_quadratic, _ = optimize.curve_fit(quadratic, volume_of_the_SDS_added, conductivity)
params_cubic, _ = optimize.curve_fit(cubic, volume_of_the_SDS_added, conductivity)

# Generate x values for plotting
xd = np.linspace(0, 25, 1000)

# Compute y values for each model
yd_piecewise = piecewise_linear(xd, *params_piecewise)
yd_linear = linear(xd, *params_linear)
yd_quadratic = quadratic(xd, *params_quadratic)
yd_cubic = cubic(xd, *params_cubic)

# Plot the data and the fits
plt.figure(figsize=(12, 8))
plt.plot(volume_of_the_SDS_added, conductivity, 'o', label="Data")
plt.plot(xd, yd_piecewise, '-', label="Piecewise Linear Fit")
plt.plot(xd, yd_linear, '--', label="Linear Fit")
plt.plot(xd, yd_quadratic, '-.', label="Quadratic Fit")
plt.plot(xd, yd_cubic, ':', label="Cubic Fit")
plt.axvline(x=params_piecewise[0], color='r', linestyle='--', label=f'CMC (Piecewise) = {params_piecewise[0]:.2f} ml')
plt.xlabel('Volume of SDS added (ml)')
plt.ylabel('Conductivity (μS)')
plt.legend()
plt.title('Comparison of Fitting Models for Critical Micelle Concentration')
plt.show()

# Print the CMC for the piecewise model
print(f"The critical micelle concentration (CMC) from the piecewise model is approximately: {params_piecewise[0]:.2f} ml")

# Print the coefficients for each model
print("\nModel Coefficients:")
print(f"Linear: a = {params_linear[0]:.4f}, b = {params_linear[1]:.4f}")
print(f"Quadratic: a = {params_quadratic[0]:.4f}, b = {params_quadratic[1]:.4f}, c = {params_quadratic[2]:.4f}")
print(f"Cubic: a = {params_cubic[0]:.4f}, b = {params_cubic[1]:.4f}, c = {params_cubic[2]:.4f}, d = {params_cubic[3]:.4f}")
