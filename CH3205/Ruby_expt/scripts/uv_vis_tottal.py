import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
import matplotlib.patches as patches
import os
from pathlib import Path
import glob

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

def process_folder(folder_path, window_length=51, polyorder=3, prominence=0.1):
    """Process all .asc files in a folder and return their data."""
    # Get all .asc files in the folder
    asc_files = glob.glob(os.path.join(folder_path, '*.asc'))
    
    if not asc_files:
        raise ValueError(f"No .asc files found in {folder_path}")
    
    # Store all spectra
    all_spectra = []
    wavelengths = None
    
    # Process each file
    for file_path in asc_files:
        w, a = read_asc_file(file_path)
        # Apply smoothing
        smoothed = savgol_filter(a, window_length, polyorder)
        
        if wavelengths is None:
            wavelengths = w
        elif not np.array_equal(wavelengths, w):
            raise ValueError(f"Wavelength mismatch in file {file_path}")
        
        all_spectra.append(smoothed)
    
    return wavelengths, np.array(all_spectra)

def plot_all_spectra(wavelengths, all_spectra, file_names=None):
    """Plot all spectra on the same graph."""
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    
    # Create color palette for multiple lines
    colors = sns.color_palette("husl", n_colors=len(all_spectra))
    
    # Plot each spectrum
    for i, spectrum in enumerate(all_spectra):
        label = f"Spectrum {i+1}" if file_names is None else file_names[i]
        plt.plot(wavelengths, spectrum, color=colors[i], alpha=0.7, linewidth=1.5, label=label)
    
    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('Absorbance', fontsize=12)
    plt.title('Overlaid UV-Vis Absorption Spectra', fontsize=14, pad=20)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout()
    
    return plt

def plot_average_spectrum(wavelengths, all_spectra, window_length=51, polyorder=3, prominence=0.1):
    """Plot the average spectrum with peak detection."""
    # Calculate average spectrum
    average_spectrum = np.mean(all_spectra, axis=0)
    
    # Find peaks in the average spectrum
    peaks, properties = find_peaks(average_spectrum, prominence=prominence)
    
    # Create the plot
    sns.set_style("whitegrid")
    plt.figure(figsize=(12, 6))
    
    # Plot average spectrum
    plt.plot(wavelengths, average_spectrum, color='#2E86C1', linewidth=2, label='Average Spectrum')
    
    # Add standard deviation area
    std_spectrum = np.std(all_spectra, axis=0)
    plt.fill_between(wavelengths, 
                    average_spectrum - std_spectrum,
                    average_spectrum + std_spectrum,
                    color='#2E86C1', alpha=0.2, label='±1 Std Dev')
    
    # Highlight peaks
    plt.plot(wavelengths[peaks], average_spectrum[peaks], 'ro', label='Peaks')
    
    # Add peak annotations
    for i, peak in enumerate(peaks):
        plt.annotate(f'{wavelengths[peak]:.1f} nm\n{average_spectrum[peak]:.3f}',
                    xy=(wavelengths[peak], average_spectrum[peak]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.5),
                    arrowprops=dict(arrowstyle='->'))
    
    plt.xlabel('Wavelength (nm)', fontsize=12)
    plt.ylabel('Absorbance', fontsize=12)
    plt.title('Average UV-Vis Absorption Spectrum', fontsize=14, pad=20)
    plt.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    
    return plt

def main():
    # Replace with your folder path containing .asc files
    folder_path = '/home/shuvam/semester_06/CH3205/Ruby_expt/UV-Vis_data'
    
    # Process all files in the folder
    wavelengths, all_spectra = process_folder(
        folder_path,
        window_length=51,
        polyorder=3,
        prominence=0.1
    )
    
    # Create overlaid spectra plot
    plot1 = plot_all_spectra(wavelengths, all_spectra)
    plot1.savefig('overlaid_spectra.png', dpi=600)
    plot1.show()
    
    # Create average spectrum plot
    plot2 = plot_average_spectrum(wavelengths, all_spectra)
    plot2.savefig('average_spectrum.png', dpi=600)
    plot2.show()

if __name__ == "__main__":
    main()