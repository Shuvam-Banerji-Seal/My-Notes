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
data['A'] = (data['Conductance in microsimen(G)'] * 1e-3) / (data['Concentration'] * 1e-3)
data['X'] = data['Concentration'] * data['A']
data['Y'] = 1 / data['A']

# Remove any rows with infinity or NaN values
data_clean = data.replace([np.inf, -np.inf], np.nan).dropna()

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(data_clean['X'], data_clean['Y'])

# Calculate confidence intervals (95%)
n = len(data_clean)
mean_x = np.mean(data_clean['X'])
se_slope = std_err * np.sqrt(n / (n * np.sum(data_clean['X']**2) - np.sum(data_clean['X'])**2))
se_intercept = std_err * np.sqrt(np.sum(data_clean['X']**2) / (n * np.sum(data_clean['X']**2) - np.sum(data_clean['X'])**2))

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
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.grid(True)

# Adjust layout to prevent legend cutoff
plt.tight_layout()

# Calculate G_o and k_a with proper error propagation
G_o = 1 / intercept
G_o_error = (se_intercept / intercept**2)  # Error propagation for 1/x

k_a = 1 / (slope * (G_o ** 2))
k_a_error = k_a * np.sqrt((se_slope/slope)**2 + 4*(se_intercept/intercept)**2)  # Error propagation

# Print results with errors
print(f"\nResults of the fitting:")
print(f"Slope = {slope:.6f} ± {se_slope:.6f}")
print(f"Intercept = {intercept:.6f} ± {se_intercept:.6f}")
print(f"G_o = {G_o:.6f} ± {G_o_error:.6f} microsimen")
print(f"k_a = {k_a:.6f} ± {k_a_error:.6f}")
print(f"Pearson R² = {r_value**2:.6f}")
print(f"p-value = {p_value:.6e}")

# Save the results to a file
with open('fitting_results.txt', 'w') as f:
    f.write(f"Results of the fitting:\n")
    f.write(f"Slope = {slope:.6f} ± {se_slope:.6f}\n")
    f.write(f"Intercept = {intercept:.6f} ± {se_intercept:.6f}\n")
    f.write(f"G_o = {G_o:.6f} ± {G_o_error:.6f} microsimen\n")
    f.write(f"k_a = {k_a:.6f} ± {k_a_error:.6f}\n")
    f.write(f"Pearson R² = {r_value**2:.6f}\n")
    f.write(f"p-value = {p_value:.6e}\n")

plt.show()