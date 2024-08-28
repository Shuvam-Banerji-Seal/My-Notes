import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Original volume data
volume_of_the_SDS_added_org = np.array([0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12, 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20, 20.5, 21, 21.5, 22, 22.5, 23, 23.5, 24, 24.5, 25])

# Convert volume to concentration (M)
volume_of_the_SDS_added = np.array([float((i * 0.04) / (60 + i)) for i in volume_of_the_SDS_added_org])

conductivity = np.array([6.2, 27.5, 38.3, 58.5, 80.7, 102.3, 122.8, 145.4, 165.4, 185.9, 204, 223, 241, 261, 275, 291, 305, 318, 332, 344, 357, 368, 379, 391, 401, 410, 419, 430, 439, 448, 457, 465, 474, 481, 490, 496, 505, 512, 521, 526, 532, 540, 546, 552, 558, 565, 571, 576, 582, 587, 592])

# Function to fit piecewise linear regression with 2 segments
def fit_piecewise_linear_two_segments(x, y):
    # Sort the data by x
    sorted_indices = np.argsort(x)
    x_sorted = x[sorted_indices]
    y_sorted = y[sorted_indices]

    # Find the best breakpoint
    best_mse = np.inf
    best_breakpoint = 0

    for i in range(1, len(x_sorted)):
        x1, y1 = x_sorted[:i], y_sorted[:i]
        x2, y2 = x_sorted[i:], y_sorted[i:]
        
        if len(x1) < 2 or len(x2) < 2:
            continue

        model1 = LinearRegression().fit(x1.reshape(-1, 1), y1)
        model2 = LinearRegression().fit(x2.reshape(-1, 1), y2)

        predictions1 = model1.predict(x1.reshape(-1, 1))
        predictions2 = model2.predict(x2.reshape(-1, 1))
        
        mse = mean_squared_error(y1, predictions1) + mean_squared_error(y2, predictions2)
        
        if mse < best_mse:
            best_mse = mse
            best_breakpoint = x_sorted[i]

    # Fit the best models
    x1_best = x_sorted[x_sorted <= best_breakpoint]
    y1_best = y_sorted[x_sorted <= best_breakpoint]
    x2_best = x_sorted[x_sorted > best_breakpoint]
    y2_best = y_sorted[x_sorted > best_breakpoint]

    model1_best = LinearRegression().fit(x1_best.reshape(-1, 1), y1_best)
    model2_best = LinearRegression().fit(x2_best.reshape(-1, 1), y2_best)

    return model1_best, model2_best, best_breakpoint

# Fit the piecewise linear model with 2 segments
model1, model2, breakpoint = fit_piecewise_linear_two_segments(volume_of_the_SDS_added, conductivity)

# Generate data for plotting
xd = np.linspace(volume_of_the_SDS_added.min(), volume_of_the_SDS_added.max(), 1000)
yd = np.zeros_like(xd)

yd[xd <= breakpoint] = model1.predict(xd[xd <= breakpoint].reshape(-1, 1))
yd[xd > breakpoint] = model2.predict(xd[xd > breakpoint].reshape(-1, 1))

# Plot the data and the piecewise linear fit
plt.figure(figsize=(8, 6), dpi=600)
plt.plot(volume_of_the_SDS_added, conductivity, 'o', label="Data")
plt.plot(xd, yd, '-', label="Piecewise Linear Fit")
plt.axvline(x=breakpoint, color='r', linestyle='--', label=f'Breakpoint = {breakpoint:.6f} M')
plt.xlabel('Concentration of SDS (M)')
plt.ylabel('Conductivity (μS)')
plt.legend()
plt.title('Dependence of Critical Micelle Concentration on Volume of SDS Added')

# Save the figure
plt.savefig('critical_micelle_concentration_piecewise_linear_two_segments.png', dpi=600)


# Print the coefficients for each segment and the breakpoint
print(f"Segment 1: Slope = {model1.coef_[0]:.2f}, Intercept = {model1.intercept_:.2f}")
print(f"Segment 2: Slope = {model2.coef_[0]:.2f}, Intercept = {model2.intercept_:.2f}")
print(f"Breakpoint: {breakpoint:.6f} M")
