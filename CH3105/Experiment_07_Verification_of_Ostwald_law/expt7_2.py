import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Read the data
data = pd.read_csv('expt7.txt', delimiter='\t')

# Constants
initial_volume = 60  # ml
concentration_stock = 0.1  # N (normality of acetic acid)
molar_mass_acetic_acid = 60.052  # g/mol

def calculate_g_eq_per_liter(volume_added):
    """
    Calculate g_eq/L considering:
    1. Convert concentration to moles
    2. Multiply by molar mass to get grams
    3. Normalize to 1L volume
    """
    total_volume = initial_volume + volume_added  # ml
    moles = (volume_added * concentration_stock) / 1000  # Convert to moles (divide by 1000 to convert ml to L)
    grams = moles * molar_mass_acetic_acid  # Convert to grams
    g_eq_per_liter = (grams * 1000) / total_volume  # Normalize to g/L (multiply by 1000 to convert L to ml)
    return g_eq_per_liter

# Calculate g_eq/L for each data point
data['g_eq_per_L'] = data['Volume of Acetic Acid(ml)'].apply(calculate_g_eq_per_liter)
print(data['g_eq_per_L'])
# Calculate 1/G (y-axis)
data['1/G'] = 1 / data['Conductance in microsimen(G)']

# Calculate G*g_eq (x-axis)
data['G*g_eq'] = data['Conductance in microsimen(G)'] * data['g_eq_per_L']

# Remove points where concentration is 0 (if present) to avoid division by zero
data_filtered = data[data['g_eq_per_L'] != 0]

# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(data_filtered['G*g_eq'], data_filtered['1/G'])

# Create the plot with larger figure size
plt.figure(figsize=(12, 8))
plt.scatter(data_filtered['G*g_eq'], data_filtered['1/G'], color='blue', label='Experimental Data')

# Generate points for the fitted line
x_fit = np.linspace(data_filtered['G*g_eq'].min(), data_filtered['G*g_eq'].max(), 100)
y_fit = slope * x_fit + intercept

# Create detailed legend text
legend_text = (
    f'Fitted Line:\n'
    f'y = ({slope:.6f} ± {std_err:.6f})x + ({intercept:.6f} ± {std_err:.6f})\n'
    f'Slope = {slope:.6f} ± {std_err:.6f}\n'
    f'Intercept = {intercept:.6f} ± {std_err:.6f}\n'
    f'Pearson R² = {r_value**2:.6f}\n'
    f'p-value = {p_value:.6e}'
)

plt.plot(x_fit, y_fit, 'r-', label=legend_text)

plt.xlabel('G*g_eq/L')
plt.ylabel('1/G')
plt.title('Conductance Fitting with g_eq/L')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
plt.grid(True)

# Adjust layout to prevent legend cutoff
plt.tight_layout()

# Calculate G_o from intercept
G_o = 1 / intercept

# Calculate k_a from slope
k_a = 1 / (slope * (G_o ** 2))

# Print results with errors
print(f"Results of the fitting:")
print(f"Slope = {slope:.6f} ± {std_err:.6f}")
print(f"Intercept (1/G_o) = {intercept:.6f} ± {std_err:.6f}")
print(f"G_o = {G_o:.6f} microsimen")
print(f"k_a = {k_a:.6f}")
print(f"Pearson R² = {r_value**2:.6f}")
print(f"p-value = {p_value:.6e}")

plt.show()

# Save the results to a file
with open('fitting_results.txt', 'w') as f:
    f.write(f"Results of the fitting:\n")
    f.write(f"Slope = {slope:.6f} ± {std_err:.6f}\n")
    f.write(f"Intercept (1/G_o) = {intercept:.6f} ± {std_err:.6f}\n")
    f.write(f"G_o = {G_o:.6f} microsimen\n")
    f.write(f"k_a = {k_a:.6f}\n")
    f.write(f"Pearson R² = {r_value**2:.6f}\n")
    f.write(f"p-value = {p_value:.6e}\n")
