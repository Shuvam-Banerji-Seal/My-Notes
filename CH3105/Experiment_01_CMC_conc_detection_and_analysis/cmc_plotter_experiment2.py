import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# File name
filename = 'experiment_1.data'

# Check if the file exists
if os.path.exists(filename):
    # Read data from text file
    data = np.loadtxt(filename, skiprows=1)  # Skips the header row
    volume_of_the_SDS_added_org = data[:, 0]
    conductivity = data[:, 1]
    print(f"Data loaded from {filename}")
else:
    
    print(f"File {filename} not found. Exiting...")
    exit()

# Convert volume to concentration (M)
volume_of_the_SDS_added = np.array([float((i * 0.04) / (60 + i)) for i in volume_of_the_SDS_added_org])

# Function to fit piecewise linear regression with the best breakpoint
def fit_piecewise_linear(x, y):
    # Sort the data by x
    sorted_indices = np.argsort(x)
    x_sorted = x[sorted_indices]
    y_sorted = y[sorted_indices]

    # Initialize variables
    best_mse = np.inf
    best_breakpoint = None
    best_model1 = None
    best_model2 = None

    # Test each possible breakpoint
    for i in range(2, len(x_sorted) - 2):  # Ensure at least 2 points in each segment
        x1, y1 = x_sorted[:i], y_sorted[:i]
        x2, y2 = x_sorted[i:], y_sorted[i:]

        model1 = LinearRegression().fit(x1.reshape(-1, 1), y1)
        model2 = LinearRegression().fit(x2.reshape(-1, 1), y2)

        predictions1 = model1.predict(x1.reshape(-1, 1))
        predictions2 = model2.predict(x2.reshape(-1, 1))

        mse = mean_squared_error(y1, predictions1) + mean_squared_error(y2, predictions2)

        if mse < best_mse:
            best_mse = mse
            best_breakpoint = x_sorted[i]
            best_model1 = model1
            best_model2 = model2

    return best_model1, best_model2, best_breakpoint

# Fit the piecewise linear model
model1, model2, breakpoint = fit_piecewise_linear(volume_of_the_SDS_added, conductivity)

# Generate data for plotting
xd = np.linspace(volume_of_the_SDS_added.min(), volume_of_the_SDS_added.max(), 1000)
yd = np.zeros_like(xd)

yd[xd <= breakpoint] = model1.predict(xd[xd <= breakpoint].reshape(-1, 1))
yd[xd > breakpoint] = model2.predict(xd[xd > breakpoint].reshape(-1, 1))

# Plot the data and the piecewise linear fit
plt.figure(figsize=(8, 6), dpi=600)
plt.plot(volume_of_the_SDS_added, conductivity, 'o', label="Data")
plt.plot(xd, yd, '-', label="Best Piecewise Linear Fit")
plt.axvline(x=breakpoint, color='r', linestyle='--', label=f'CMC Breakpoint = {breakpoint:.6f} M')
plt.xlabel('Concentration of SDS (M)')
plt.ylabel('Conductivity (μS)')
plt.legend()
plt.title('Determination of CMC via Best Piecewise Linear Fit')

# Save the figure
plt.savefig('best_piecewise_linear_cmc.png', dpi=600)

# Print the coefficients for each segment and the breakpoint
print(f"Segment 1: Slope = {model1.coef_[0]:.2f}, Intercept = {model1.intercept_:.2f}")
print(f"Segment 2: Slope = {model2.coef_[0]:.2f}, Intercept = {model2.intercept_:.2f}")
print(f"CMC Breakpoint: {breakpoint:.6f} M")
