import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# Given data
vol_added_uL = np.array([0, 50, 100, 150, 200])  # Volume of quencher added in µL
imax = np.array([297200, 289850, 285050, 279570, 277290])  # Fluorescence intensity (Imax)
area = np.array([2.56419, 2.51063, 2.48472, 2.41514, 2.4122])  # Area

# Initial conditions
initial_volume_mL = 3.0  # Initial solution volume in mL
initial_conc = 1e-4  # Initial concentration in M

# Calculate quencher concentrations
# Convert added volumes to mL for calculation
vol_added_mL = vol_added_uL / 1000

# Total volume after each addition
total_volume_mL = initial_volume_mL + vol_added_mL

# Calculate quencher concentration
# Assuming the quencher is pure (adjust concentration if needed)
quencher_conc = ((vol_added_mL*initial_conc) / total_volume_mL)  # Molar fraction of quencher

# Calculate F0/F ratios for both intensity and area
f0_f_intensity = imax[0] / imax
f0_f_area = area[0] / area

# Linear fit function for Stern-Volmer plot
def linear_fit(x, m, b):
    return m * x + b

# Perform linear regression for intensity data
params_intensity, _ = curve_fit(linear_fit, quencher_conc, f0_f_intensity)
ksv_intensity = params_intensity[0]

# Perform linear regression for area data
params_area, _ = curve_fit(linear_fit, quencher_conc, f0_f_area)
ksv_area = params_area[0]

# Create x values for the fit line
x_fit = np.linspace(0, max(quencher_conc), 100)
y_fit_intensity = linear_fit(x_fit, *params_intensity)
y_fit_area = linear_fit(x_fit, *params_area)

# Create plot
plt.figure(figsize=(10, 6))

# Plot intensity data
plt.subplot(1, 2, 1)
plt.scatter(quencher_conc, f0_f_intensity, color='blue', marker='o', label='Data')
plt.plot(x_fit, y_fit_intensity, 'r-', label=f'Fit: Ksv = {ksv_intensity:.2f}')
plt.xlabel('Quencher Molar Fraction')
plt.ylabel('F₀/F (Intensity)')
plt.title('Stern-Volmer Plot (Using Intensity)')
plt.grid(True, alpha=0.3)
plt.legend()

# Plot area data
plt.subplot(1, 2, 2)
plt.scatter(quencher_conc, f0_f_area, color='green', marker='o', label='Data')
plt.plot(x_fit, y_fit_area, 'r-', label=f'Fit: Ksv = {ksv_area:.2f}')
plt.xlabel('Quencher Molar Fraction')
plt.ylabel('F₀/F (Area)')
plt.title('Stern-Volmer Plot (Using Area)')
plt.grid(True, alpha=0.3)
plt.legend()

plt.tight_layout()

# Print results
print(f"Stern-Volmer Constant (using intensity): Ksv = {ksv_intensity:.4f}")
print(f"Stern-Volmer Constant (using area): Ksv = {ksv_area:.4f}")

# If you want to see the data table used for calculations
print("\nCalculated values:")
print("Vol Added (µL) | Quencher Molar Fraction | F0/F (Intensity) | F0/F (Area)")
for i in range(len(vol_added_uL)):
    print(f"{vol_added_uL[i]:11.0f} | {quencher_conc[i]:21.6f} | {f0_f_intensity[i]:15.4f} | {f0_f_area[i]:9.4f}")

plt.show()