import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Read the data
data = pd.read_csv('expt7.txt', delimiter='\t')

# Calculate concentration (c) from volume
initial_volume = 60  # ml
concentration_stock = 0.1  # N (normality of acetic acid)

def calculate_concentration(volume_added):
    # if volume_added == 0:
    #     return 0
    total_volume = initial_volume + volume_added
    concentration = (volume_added * concentration_stock) / total_volume
    print(f"concentration : {concentration}")
    return concentration

# Calculate concentrations
data['Concentration'] = data['Volume of Acetic Acid(ml)'].apply(calculate_concentration)

#Coverting to G_eq by multiplying molar mass of acetic acid and the volume
def calculate_volume(volume_added):
    total_volume = initial_volume + volume_added
    return total_volume


# Calculate 1/G (y-axis)
data['1/G'] = 1 / (data['Conductance in microsimen(G)'].apply(calculate_volume)*60.052)  


        #data ['1/G'] = data['Conductance in microsimen(G)']
# Calculate G*c (x-axis)
data['G*c'] = (data['Conductance in microsimen(G)'].apply(calculate_volume)*60.052) * data['Concentration']

# Remove the point where concentration is 0 (if present) to avoid division by zero
data_filtered = data[data['Concentration'] != 0]

print(data['Conductance in microsimen(G)'])
print(data['Concentration'])
print(data['1/G'])
print(data['G*c'])




# Perform linear regression
slope, intercept, r_value, p_value, std_err = stats.linregress(data_filtered['G*c'], data_filtered['1/G'])

# Create the plot with larger figure size
plt.figure(figsize=(12, 8))
plt.scatter(data_filtered['G*c'], data_filtered['1/G'], color='blue', label='Experimental Data')

# Generate points for the fitted line
x_fit = np.linspace(data_filtered['G*c'].min(), data_filtered['G*c'].max(), 100)
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

plt.xlabel('G*c')
plt.ylabel('1/G')
plt.title('Conductance Fitting')
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
