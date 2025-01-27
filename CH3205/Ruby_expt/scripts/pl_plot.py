import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter, find_peaks
from matplotlib.gridspec import GridSpec

def analyze_photoluminescence(file_path, 
                            savgol_window=11,
                            savgol_polyorder=3,
                            peak_prominence=None,
                            peak_distance=10):
    """
    Analyzes photoluminescence data with advanced smoothing and peak detection.
    
    Parameters:
    -----------
    file_path : str
        Path to the .dat file containing PL data
    savgol_window : int
        Window length for Savitzky-Golay filter (must be odd)
    savgol_polyorder : int
        Polynomial order for Savitzky-Golay filter
    peak_prominence : float or None
        Minimum peak prominence. If None, calculated as 5% of data range
    peak_distance : int
        Minimum number of points between peaks
    """
    try:
        # Read the data
        data = pd.read_csv(file_path, delim_whitespace=True, skiprows=2, 
                          header=None, names=["Wavelength", "CPS"])
        
        # Ensure savgol_window is odd
        if savgol_window % 2 == 0:
            savgol_window += 1
            
        # Apply smoothing
        smoothed_cps = savgol_filter(data["CPS"], 
                                   window_length=savgol_window, 
                                   polyorder=savgol_polyorder)
        
        # Calculate automatic prominence if not specified
        if peak_prominence is None:
            peak_prominence = (np.max(smoothed_cps) - np.min(smoothed_cps)) * 0.05
        
        # Find peaks with more controlled parameters
        peaks, peak_properties = find_peaks(smoothed_cps,
                                          prominence=peak_prominence,
                                          distance=peak_distance,
                                          width=3)
        
        # Create figure with two subplots and an extra space for residuals explanation
        fig = plt.figure(figsize=(12, 10))
        gs = GridSpec(3, 1, height_ratios=[3, 1, 0.5], hspace=0.4)
        
        # Main plot
        ax1 = fig.add_subplot(gs[0])
        
        # Plot in specific order for correct layering:
        # 1. Raw data points
        ax1.plot(data["Wavelength"], data["CPS"], 'o', 
                color='lightgray', markersize=4, label='Raw Data', zorder=1)
        
        # 2. Smoothed line
        ax1.plot(data["Wavelength"], smoothed_cps, 
                'b-', linewidth=2, label='Smoothed Data', zorder=2)
        
        # 3. Peak markers on top
        ax1.scatter(data["Wavelength"].iloc[peaks], smoothed_cps[peaks], 
                   color='red', s=100, marker='^', label='Peaks', zorder=3)
        
        # Add peak labels
        for idx, peak in enumerate(peaks):
            ax1.annotate(f'Peak {idx+1}',
                        xy=(data["Wavelength"].iloc[peak], smoothed_cps[peak]),
                        xytext=(10, 10), textcoords='offset points',
                        fontsize=8, color='darkred', zorder=3)
        
        ax1.set_title('Photoluminescence Spectrum Analysis', 
                     fontsize=16, fontweight='bold', pad=20)
        ax1.set_xlabel('Wavelength (nm)', fontsize=12)
        ax1.set_ylabel('Intensity (CPS)', fontsize=12)
        ax1.grid(True, linestyle='--', alpha=0.7)
        ax1.legend(loc='upper right')
        
        # Residuals plot
        ax2 = fig.add_subplot(gs[1])
        residuals = data["CPS"] - smoothed_cps
        ax2.plot(data["Wavelength"], residuals, 
                'k-', linewidth=1, label='Residuals', zorder=1)
        ax2.fill_between(data["Wavelength"], residuals, 
                        alpha=0.3, color='gray', zorder=2)
        ax2.axhline(y=0, color='r', linestyle='--', alpha=0.5, zorder=3)
        ax2.set_xlabel('Wavelength (nm)', fontsize=12)
        ax2.set_ylabel('Residuals\n(Raw - Smoothed)', fontsize=12)
        ax2.grid(True, linestyle='--', alpha=0.7)
        
        # Add residuals explanation
        # ax3 = fig.add_subplot(gs[2])
        # ax3.axis('off')
        # explanation = ("Residuals Plot Explanation:\n"
        #               "• Shows the difference between raw and smoothed data at each point\n"
        #               "• Values close to zero (red dashed line) indicate good fit\n"
        #               "• Large residuals show where smoothing deviates from raw data")
        # ax3.text(0.1, 0.2, explanation, fontsize=10, 
        #         verticalalignment='center', horizontalalignment='left',
        #         bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        
        plt.savefig('pl_22ms016.png', dpi=600)
        plt.show()
        
        # Print peak information
        print("\nPeak Analysis Results:")
        print("-" * 50)
        for idx, peak in enumerate(peaks):
            wavelength = data["Wavelength"].iloc[peak]
            intensity = smoothed_cps[peak]
            prominence = peak_properties["prominences"][idx]
            width = peak_properties["widths"][idx]
            
            print(f"\nPeak {idx+1}:")
            print(f"Wavelength: {wavelength:.2f} nm")
            print(f"Intensity: {intensity:.2f} CPS")
            print(f"Prominence: {prominence:.2f}")
            print(f"Width: {width:.2f} points")
        
        return data["Wavelength"].iloc[peaks], smoothed_cps[peaks], peak_properties
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None, None, None

# Example usage
file_path = "/home/shuvam/semester_06/CH3205/Ruby_expt/PL_data/22ms016.dat"
analyze_photoluminescence(file_path,
                         savgol_window=11,
                         savgol_polyorder=3,
                         peak_distance=10)