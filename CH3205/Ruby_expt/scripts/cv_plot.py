import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks

def parse_cv_data(filepath):
    """Parse CV data files, ensuring numeric data and handling edge cases."""
    with open(filepath, 'r') as f:
        lines = f.readlines()
    
    numeric_lines = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) != 2:
            continue
        try:
            float(parts[0]), float(parts[1])
            numeric_lines.append(parts)
        except ValueError:
            continue
    
    data = pd.DataFrame(numeric_lines, columns=['Potential', 'Current']).astype(float)
    return data
# --------------------------
# Ferrocene Standardization
# --------------------------
def calculate_e_half(data):
    """Calculate E1/2 for a reversible redox couple (e.g., ferrocene)."""
    current = data['Current']
    epa_index = current.idxmax()  # Anodic peak (oxidation)
    epc_index = current.idxmin()  # Cathodic peak (reduction)
    epa = data['Potential'].iloc[epa_index]
    epc = data['Potential'].iloc[epc_index]
    return (epa + epc) / 2  # E1/2 = (Epa + Epc)/2

def find_all_peaks(potential, current, prominence=0.05, width=None, height=None, distance=None):
    """
    Find all significant peaks in CV data with enhanced sensitivity for smaller features.
    
    Parameters:
    - prominence: Lower value to detect smaller peaks (default 0.05 instead of 0.1)
    - width: Minimum peak width
    - height: Minimum peak height
    - distance: Minimum distance between peaks
    """
    # Normalize current for better peak detection
    current_range = np.ptp(current)
    
    # Find maxima (oxidation peaks) with more sensitive parameters
    max_peaks, max_properties = find_peaks(current,
                                         prominence=prominence*current_range,
                                         width=width,
                                         height=height,
                                         distance=distance)
    
    # Find minima (reduction peaks) with more sensitive parameters
    min_peaks, min_properties = find_peaks(-current,
                                         prominence=prominence*current_range,
                                         width=width,
                                         height=height,
                                         distance=distance)
    
    # Sort peaks by current magnitude to distinguish major and minor peaks
    oxidation_peaks = list(zip(potential[max_peaks], current[max_peaks]))
    reduction_peaks = list(zip(potential[min_peaks], current[min_peaks]))
    
    return {
        'oxidation': sorted(oxidation_peaks, key=lambda x: abs(x[1]), reverse=True),
        'reduction': sorted(reduction_peaks, key=lambda x: abs(x[1]), reverse=True)
    }


def calculate_e_half(data):
    """Calculate E1/2 for a reversible redox couple."""
    current = data['Current']
    epa_index = current.idxmax()  # Anodic peak
    epc_index = current.idxmin()  # Cathodic peak
    epa = data['Potential'].iloc[epa_index]
    epc = data['Potential'].iloc[epc_index]
    return (epa + epc) / 2

# Load and process data
fc_data = parse_cv_data('/home/shuvam/semester_06/CH3205/Ruby_expt/CV/Fc_standardization.txt')
ru_anodic_data = parse_cv_data('/home/shuvam/semester_06/CH3205/Ruby_expt/CV/Ru(BPY)3_Anodic_Final.txt')
ru_cathodic_data = parse_cv_data('/home/shuvam/semester_06/CH3205/Ruby_expt/CV/Ru(BPY)3_Cathodic_Final.txt')

# Calculate Fc correction
e_half_fc = calculate_e_half(fc_data)
delta_e = e_half_fc - 0.0

# Create standardized potential columns
ru_anodic_data['Potential_vs_Fc'] = ru_anodic_data['Potential'] - delta_e
ru_cathodic_data['Potential_vs_Fc'] = ru_cathodic_data['Potential'] - delta_e

# Modified plotting code for better peak visualization
def plot_cv_with_peaks(ax, datasets, standardized=False):
    """Enhanced plotting function with better peak detection and visualization"""
    for dataset, label, color in datasets:
        # Plot the CV curve
        potential = dataset['Potential_vs_Fc'] if standardized else dataset['Potential']
        ax.plot(potential, dataset['Current'] * 1e6,
                label=label, color=color, linewidth=2)
        
        # Find peaks with more sensitive parameters
        peaks = find_all_peaks(potential.values, dataset['Current'].values,
                             prominence=0.03,  # More sensitive prominence
                             width=5,          # Minimum peak width
                             distance=20)      # Minimum distance between peaks
        
        # Plot peaks with different markers for major and minor peaks
        for peak_type in ['oxidation', 'reduction']:
            for i, (pot, curr) in enumerate(peaks[peak_type]):
                # Determine if it's a major or minor peak based on current magnitude
                is_major = i < 2  # First two peaks are considered major
                
                marker_size = 150 if is_major else 100
                marker_style = '*' if is_major else 'o'
                
                ax.scatter(pot, curr * 1e6, 
                          color=color, 
                          marker=marker_style, 
                          s=marker_size, 
                          zorder=5)
                
                # Adjust annotation position and style
                xytext = (-10, 5) if peak_type == 'oxidation' else (10, -10)
                peak_label = f'Major {peak_type}' if is_major else f'Minor {peak_type}'
                
                ax.annotate(f'{pot:.3f} V',
                           xy=(pot, curr * 1e6),
                           xytext=xytext,
                           textcoords='offset points',
                           fontsize=8,
                           bbox=dict(facecolor='white', edgecolor='none', alpha=0.7))

# Create the plots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 12), height_ratios=[1, 1])

# Plot 1: Non-standardized data
datasets_orig = [
    (ru_anodic_data, 'Ru(bpy)₃²⁺ Anodic', '#FF4500'),
    (ru_cathodic_data, 'Ru(bpy)₃²⁺ Cathodic', '#1E90FF')
]
plot_cv_with_peaks(ax1, datasets_orig, standardized=False)

# Plot 2: Standardized data
datasets_std = [
    (ru_anodic_data, 'Ru(bpy)₃²⁺ Anodic', '#FF4500'),
    (ru_cathodic_data, 'Ru(bpy)₃²⁺ Cathodic', '#1E90FF')
]
# Plot Fc reference first
ax2.plot(fc_data['Potential'] - delta_e, fc_data['Current'] * 1e6,
         label='Ferrocene (Fc)', color='grey', linewidth=1.5, alpha=0.7)
plot_cv_with_peaks(ax2, datasets_std, standardized=True)


# Customize plots
ax1.set_title('Non-standardized Cyclic Voltammogram vs. Ag/AgCl', fontsize=12)
ax1.set_xlabel('Potential vs. Ag/AgCl (V)', fontsize=10)
ax1.set_ylabel('Current (μA)', fontsize=10)
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(loc='best', fontsize=9)

# Add reference lines and customize standardized plot
ax2.axvline(x=0, color='black', linestyle='--', linewidth=1, label='Fc/Fc⁺ (0 V)')
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.set_title('Standardized Cyclic Voltammogram vs. Fc/Fc⁺', fontsize=12)
ax2.set_xlabel('Potential vs. Fc/Fc⁺ (V)', fontsize=10)
ax2.set_ylabel('Current (μA)', fontsize=10)
ax2.grid(True, linestyle='--', alpha=0.3)
ax2.legend(loc='best', fontsize=9)

# Add experimental details
info_text = (
    f"Ferrocene E₁/₂: {e_half_fc:.3f} V vs. Ag/AgCl\n"
    f"Potential shift: {delta_e:.3f} V\n"
    "Scan rate: 100 mV/s\n"
)
plt.figtext(0.85, 0.19, info_text, fontsize=8, bbox=dict(facecolor='white', alpha=0.8), ha='right', va='center')


plt.savefig('cv_comparison_all_peaks.png', dpi=900)
plt.show()