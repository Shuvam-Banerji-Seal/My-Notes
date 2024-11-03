import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Read the data
data = pd.read_csv('expt7.txt', delimiter='\t')

# Calculate concentration from volume
initial_volume = 60  # ml
concentration_stock = 0.1  # N (normality of acetic acid)

def calculate_concentration(volume_added):
    total_volume = initial_volume + volume_added
    concentration = (volume_added * concentration_stock) / total_volume
    return concentration

# Calculate concentrations
data['Concentration'] = data['Volume of Acetic Acid(ml)'].apply(calculate_concentration)

# Calculate the required parameters
data['A'] = (data['Conductance in microsimen(G)'] * 1e-6) / (data['Concentration'])
data['X'] = data['Concentration'] * data['A']
data['Y'] = 1 / data['A']

# Remove any rows with infinity or NaN values
data_clean = data.replace([np.inf, -np.inf], np.nan).dropna()

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(data_clean['X'], data_clean['Y'])

# Correct calculation of standard errors for slope and intercept
n = len(data_clean)
x = data_clean['X']
y = data_clean['Y']

# Calculate residuals
y_pred = slope * x + intercept
residuals = y - y_pred

# Calculate sum of squared residuals
ss_residuals = np.sum(residuals**2)

# Calculate degrees of freedom
df = n - 2

# Calculate mean squared error
mse = ss_residuals / df

# Calculate sum of squared deviations of x from its mean
x_mean = np.mean(x)
ss_xx = np.sum((x - x_mean)**2)

# Calculate standard errors
se_slope = np.sqrt(mse / ss_xx)
se_intercept = np.sqrt(mse * (1/n + x_mean**2/ss_xx))

# Create the plot with larger figure size
plt.figure(figsize=(12, 8))
plt.scatter(data_clean['X'], data_clean['Y'], color='blue', label='Experimental Data')

# Generate points for the fitted line
x_fit = np.linspace(data_clean['X'].min(), data_clean['X'].max(), 100)
y_fit = slope * x_fit + intercept

# Create detailed legend text with proper error reporting
legend_text = (
    f'Fitted Line:\n'
    f'y = ({slope:.6f} ± {se_slope:.6f})x + ({intercept:.6f} ± {se_intercept:.6f})\n'
    f'Slope = {slope:.6f} ± {se_slope:.6f}\n'
    f'Intercept = {intercept:.6f} ± {se_intercept:.6f}\n'
    f'Pearson R² = {r_value**2:.6f}\n'
    f'p-value = {p_value:.6e}'
)

plt.plot(x_fit, y_fit, 'r-', label=legend_text)

plt.xlabel('λc (Concentration × Molar Conductance)')
plt.ylabel('1/λ (1/Molar Conductance)')
plt.title('Conductance Analysis')
# Updated legend position to top left inside the plot
plt.legend(loc='upper left')
plt.grid(True)

# Calculate A_o and k_a with proper error propagation
A_o = 1 / intercept
# Error propagation for A_o (1/intercept)
A_o_error = A_o * (se_intercept / abs(intercept))

k_a = 1 / (slope * (A_o ** 2))
# Error propagation for k_a using partial derivatives
k_a_error = k_a * np.sqrt((se_slope/slope)**2 + 4*(se_intercept/intercept)**2)

# Print results with errors
print(f"\nResults of the fitting:")
print(f"Slope = {slope:.6f} ± {se_slope:.6f}")
print(f"Intercept = {intercept:.6f} ± {se_intercept:.6f}")
print(f"A_o = {A_o:.6f} ± {A_o_error:.6f} microsimen")
print(f"k_a x 10^-5 = {k_a*1e5:.6f} ± {k_a_error*1e5:.6f}")
print(f"Pearson R² = {r_value**2:.6f}")
print(f"p-value = {p_value:.6e}")

# Save the results to a file
with open('fitting_results.txt', 'w') as f:
    f.write(f"Results of the fitting:\n")
    f.write(f"Slope = {slope:.6f} ± {se_slope:.6f}\n")
    f.write(f"Intercept = {intercept:.6f} ± {se_intercept:.6f}\n")
    f.write(f"A_o = {A_o:.6f} ± {A_o_error:.6f} microsimen\n")
    f.write(f"k_a = {k_a:.6f} ± {k_a_error:.6f}\n")
    f.write(f"Pearson R² = {r_value**2:.6f}\n")
    f.write(f"p-value = {p_value:.6e}\n")
plt.savefig('fig_expt7.png', dpi=800)
plt.show()
