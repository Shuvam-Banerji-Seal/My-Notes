import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import stats

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

# Calculate quencher concentration using your correction
quencher_conc = (vol_added_mL * initial_conc) / total_volume_mL  # Molar fraction of quencher

# Calculate F0/F ratios for both intensity and area
f0_f_intensity = imax[0] / imax
f0_f_area = area[0] / area

# Linear fit function for Stern-Volmer plot
def linear_fit(x, m, b):
    return m * x + b

# Perform linear regression for intensity data
params_intensity, covariance_intensity = curve_fit(linear_fit, quencher_conc, f0_f_intensity)
ksv_intensity = params_intensity[0]
b_intensity = params_intensity[1]

# Calculate errors for intensity parameters
perr_intensity = np.sqrt(np.diag(covariance_intensity))
ksv_intensity_err = perr_intensity[0]
b_intensity_err = perr_intensity[1]

# Calculate R² for intensity data
residuals_intensity = f0_f_intensity - linear_fit(quencher_conc, *params_intensity)
ss_res_intensity = np.sum(residuals_intensity**2)
ss_tot_intensity = np.sum((f0_f_intensity - np.mean(f0_f_intensity))**2)
r_squared_intensity = 1 - (ss_res_intensity / ss_tot_intensity)

# Calculate Pearson's r for intensity data
r_intensity, p_intensity = stats.pearsonr(quencher_conc, f0_f_intensity)

# Perform linear regression for area data
params_area, covariance_area = curve_fit(linear_fit, quencher_conc, f0_f_area)
ksv_area = params_area[0]
b_area = params_area[1]

# Calculate errors for area parameters
perr_area = np.sqrt(np.diag(covariance_area))
ksv_area_err = perr_area[0]
b_area_err = perr_area[1]

# Calculate R² for area data
residuals_area = f0_f_area - linear_fit(quencher_conc, *params_area)
ss_res_area = np.sum(residuals_area**2)
ss_tot_area = np.sum((f0_f_area - np.mean(f0_f_area))**2)
r_squared_area = 1 - (ss_res_area / ss_tot_area)

# Calculate Pearson's r for area data
r_area, p_area = stats.pearsonr(quencher_conc, f0_f_area)

# Create x values for the fit line
x_fit = np.linspace(0, max(quencher_conc), 100)
y_fit_intensity = linear_fit(x_fit, *params_intensity)
y_fit_area = linear_fit(x_fit, *params_area)

# Create plot
plt.figure(figsize=(12, 8))

# Plot intensity data
plt.subplot(1, 2, 1)
plt.scatter(quencher_conc, f0_f_intensity, color='blue', marker='o', label='Data')
plt.plot(x_fit, y_fit_intensity, 'r-', label=f'Fit: Ksv = {ksv_intensity:.2f}')
plt.xlabel('Quencher Concentration (M)', fontsize=12)
plt.ylabel('F₀/F (Intensity)', fontsize=12)
plt.title('Stern-Volmer Plot (Using Intensity)', fontsize=14)
plt.grid(True, alpha=0.3)

# Add statistical parameters to the plot
stats_text = f"Ksv = {ksv_intensity:.4f} ± {ksv_intensity_err:.4f}\n"
stats_text += f"Intercept = {b_intensity:.4f} ± {b_intensity_err:.4f}\n"
stats_text += f"R² = {r_squared_intensity:.4f}\n"
stats_text += f"Pearson r = {r_intensity:.4f}\n"
stats_text += f"p-value = {p_intensity:.4e}"
plt.annotate(stats_text, xy=(0.05, 0.65), xycoords='axes fraction', 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
plt.legend()

# Plot area data
plt.subplot(1, 2, 2)
plt.scatter(quencher_conc, f0_f_area, color='green', marker='o', label='Data')
plt.plot(x_fit, y_fit_area, 'r-', label=f'Fit: Ksv = {ksv_area:.2f}')
plt.xlabel('Quencher Concentration (M)', fontsize=12)
plt.ylabel('F₀/F (Area)', fontsize=12)
plt.title('Stern-Volmer Plot (Using Area)', fontsize=14)
plt.grid(True, alpha=0.3)

# Add statistical parameters to the plot
stats_text = f"Ksv = {ksv_area:.4f} ± {ksv_area_err:.4f}\n"
stats_text += f"Intercept = {b_area:.4f} ± {b_area_err:.4f}\n"
stats_text += f"R² = {r_squared_area:.4f}\n"
stats_text += f"Pearson r = {r_area:.4f}\n"
stats_text += f"p-value = {p_area:.4e}"
plt.annotate(stats_text, xy=(0.05, 0.65), xycoords='axes fraction', 
             bbox=dict(boxstyle="round,pad=0.5", facecolor="white", alpha=0.8))
plt.legend()

plt.tight_layout()

# Print comprehensive results
print(f"===== Stern-Volmer Analysis Results =====")
print("\nUsing Intensity Data:")
print(f"Stern-Volmer Constant (Ksv): {ksv_intensity:.6f} ± {ksv_intensity_err:.6f}")
print(f"Y-intercept: {b_intensity:.6f} ± {b_intensity_err:.6f}")
print(f"Coefficient of determination (R²): {r_squared_intensity:.6f}")
print(f"Pearson correlation coefficient (r): {r_intensity:.6f}")
print(f"p-value: {p_intensity:.6e}")

print("\nUsing Area Data:")
print(f"Stern-Volmer Constant (Ksv): {ksv_area:.6f} ± {ksv_area_err:.6f}")
print(f"Y-intercept: {b_area:.6f} ± {b_area_err:.6f}")
print(f"Coefficient of determination (R²): {r_squared_area:.6f}")
print(f"Pearson correlation coefficient (r): {r_area:.6f}")
print(f"p-value: {p_area:.6e}")

# Data table with calculated values
print("\nCalculated values:")
print("Vol Added (µL) | Quencher Conc (M) | F0/F (Intensity) | F0/F (Area)")
print("-------------|-----------------|-----------------|------------")
for i in range(len(vol_added_uL)):
    print(f"{vol_added_uL[i]:11.0f} | {quencher_conc[i]:15.8e} | {f0_f_intensity[i]:15.4f} | {f0_f_area[i]:9.4f}")

plt.show()