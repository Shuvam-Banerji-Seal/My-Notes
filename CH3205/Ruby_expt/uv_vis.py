import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
import matplotlib.patches as patches

def read_asc_file(file_path):
    """Read .asc file and extract spectral data after #DATA line."""
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    # Find the #DATA line
    data_start = 0
    for i, line in enumerate(lines):
        if '#DATA' in line:
            data_start = i + 1
            break
    
    # Extract data after #DATA
    wavelengths = []
    absorbance = []
    for line in lines[data_start:]:
        if line.strip():  # Skip empty lines
            w, a = map(float, line.strip().split())
            wavelengths.append(w)
            absorbance.append(a)
    
    return np.array(wavelengths), np.array(absorbance)

def plot_uv_vis_spectrum(file_path, window_length=51, polyorder=3, prominence=0.1):
    """Plot UV-Vis spectrum with smoothing and peak detection."""
    # Read data
    wavelengths, absorbance = read_asc_file(file_path)
    
    # Apply Savitzky-Golay smoothing
    smoothed = savgol_filter(absorbance, window_length, polyorder)
    
    # Find peaks
    peaks, properties = find_peaks(smoothed, prominence=prominence)
    
    # Set up the plot style
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    
    # Create the main plot
    ax = plt.gca()
    
    # Plot original data with low opacity
    # plt.plot(wavelengths, absorbance, color='#ffff00', alpha=1, label='Original Data')
    
    # Plot smoothed data
    plt.plot(wavelengths, smoothed, color='#2E86C1', linewidth=2, label='Smoothed Data')
    
    # Highlight peaks
    plt.plot(wavelengths[peaks], smoothed[peaks], 'ro', label='Peaks')
    
    # Add peak annotations
    for i, peak in enumerate(peaks):
        plt.annotate(f'{wavelengths[peak]:.1f} nm\n{smoothed[peak]:.3f}',
                    xy=(wavelengths[peak], smoothed[peak]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->'))
    
    # Customize the plot
    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('Absorbance', fontsize=12)
    plt.title('UV-Vis Absorption Spectrum', fontsize=14, pad=20)
    
    # Add legend
    plt.legend(loc='upper right', frameon=True)
    
    
    
    return plt

def main():
    # Replace with your .asc file path
    file_path = '/home/shuvam/semester_06/CH3205/Ruby_expt/UV-Vis_data/CH-3205_22ms140.asc'
    
    # Create plot
    plot = plot_uv_vis_spectrum(
        file_path,
        window_length=51,  # Adjust smoothing window
        polyorder=3,       # Polynomial order for smoothing
        prominence=0.1     # Adjust peak detection sensitivity
    )
    
    # Show plot
    plt.savefig('uv_vis_22ms076.png', dpi=600)
    plot.show()
    

if __name__ == "__main__":
    main()