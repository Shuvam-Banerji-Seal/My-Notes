import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks, savgol_filter
from scipy.constants import h, physical_constants
import traceback # Import traceback for detailed error reporting

# --- Constants ---
bohr_magneton = physical_constants['Bohr magneton'][0] # J/T
# Planck constant (h) is imported from scipy.constants

# --- Configuration ---
# !!! Important: Set the correct microwave frequency used during the experiment !!!
MICROWAVE_FREQUENCY_GHZ = 9.5  # Example: X-band frequency in GHz
FILE_PATH = 'VoACAC.asc' # <<< --- CHANGE THIS TO YOUR ACTUAL FILE PATH --- >>>

# --- Functions ---

def read_epr_asc(filepath, header_lines_to_skip=3): # *** CHANGED default to 3 ***
    """
    Reads an EPR .asc file, skipping header lines and ensuring numeric conversion.
    Assumes header lines followed by a line with column names, then data.

    Args:
        filepath (str): Path to the .asc file.
        header_lines_to_skip (int): Number of lines to skip at the beginning
                                    (including descriptive headers AND the column name line).

    Returns:
        tuple: (magnetic_field, intensity) as numpy arrays, or (None, None) on error.
    """
    try:
        print(f"Attempting to read file: {filepath}, skipping {header_lines_to_skip} lines.")
        # Read data using pandas, skipping header AND column name line, using whitespace delimiter
        data = pd.read_csv(
            filepath,
            skiprows=header_lines_to_skip, # Skip descriptive headers AND the line like "X [G] Intensity"
            delim_whitespace=True,
            names=['MagneticField_G', 'Intensity'], # Provide the column names explicitly
            engine='python', # Use python engine for flexible whitespace handling
            on_bad_lines='warn' # Report lines that cause parsing issues
        )
        print(f"Initial read successful. DataFrame head:\n{data.head()}") # Print head after initial read

        # --- Explicitly convert columns to numeric, coercing errors ---
        # This attempts to convert each value; if it fails, it becomes NaN
        data['MagneticField_G'] = pd.to_numeric(data['MagneticField_G'], errors='coerce')
        data['Intensity'] = pd.to_numeric(data['Intensity'], errors='coerce')

        # --- Check for and handle conversion errors (NaNs) ---
        # isnull().any() checks if any NaN exists per column, .any() checks across columns
        if data.isnull().any().any():
            print(f"Warning: Non-numeric data found in file '{filepath}' after initial read. Rows with errors:")
            # Print rows where *any* column has NaN after conversion attempt
            print(data[data.isnull().any(axis=1)])
            # Option: Drop rows with NaN values to proceed with valid data
            original_count = len(data)
            data.dropna(inplace=True)
            print(f"Dropped {original_count - len(data)} rows with non-numeric data.")
            # Option 2: Raise an error if any non-numeric data is unacceptable (uncomment below)
            # raise ValueError("Non-numeric data found in file after header. Cannot proceed.")

        # Check if DataFrame is empty after dropping rows
        if data.empty:
             print(f"Error: No valid numeric data remains in '{filepath}' after handling errors.")
             return None, None

        # Convert Gauss to Tesla for calculations (1 G = 1e-4 T)
        # Now this should work as data contains only valid numbers
        magnetic_field_T = data['MagneticField_G'].values * 1e-4
        intensity = data['Intensity'].values
        print(f"Successfully read and processed {len(magnetic_field_T)} data points from {filepath}")
        return magnetic_field_T, intensity

    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None, None
    except ValueError as ve: # Catch potential error from explicit conversion/handling
         print(f"Error processing file data in '{filepath}': {ve}")
         return None, None
    except Exception as e:
        # Add more specific error reporting for unexpected issues
        print(f"An unexpected error occurred while reading file {filepath}:")
        print(traceback.format_exc()) # Print detailed traceback
        return None, None


def calculate_derivative(magnetic_field, intensity, smooth_window=11, smooth_polyorder=3):
    """
    Calculates the first derivative of the intensity, optionally smoothing first.

    Args:
        magnetic_field (np.array): Magnetic field values (Tesla).
        intensity (np.array): Intensity values.
        smooth_window (int): Window size for Savitzky-Golay filter (odd integer > polyorder).
                               Set to None or 0 to disable smoothing.
        smooth_polyorder (int): Polynomial order for Savitzky-Golay filter.

    Returns:
        np.array: First derivative of intensity with respect to magnetic field.
    """
    if smooth_window and smooth_window > smooth_polyorder and len(intensity) > smooth_window:
        try:
            intensity_smoothed = savgol_filter(intensity, smooth_window, smooth_polyorder)
            print(f"Applied Savitzky-Golay smoothing (window={smooth_window}, order={smooth_polyorder})")
        except ValueError as e:
            print(f"Warning: Smoothing failed ({e}). Calculating derivative on raw data.")
            intensity_smoothed = intensity # Fallback to raw data
    else:
        if smooth_window:
             print("Smoothing disabled (window size too small or invalid).")
        intensity_smoothed = intensity # No smoothing or invalid parameters

    # Calculate the derivative using numpy.gradient
    # np.gradient calculates the gradient using central differences (except at boundaries)
    derivative = np.gradient(intensity_smoothed, magnetic_field)
    return derivative

def calculate_g_value(field_T, frequency_Hz):
    """
    Calculates the g-value from the resonance field and frequency.
    g = h * nu / (mu_B * B_res)

    Args:
        field_T (float or np.array): Resonance magnetic field(s) in Tesla.
        frequency_Hz (float): Microwave frequency in Hz.

    Returns:
        float or np.array: Calculated g-value(s). Returns np.nan on error.
    """
    # Check for None, zero, or negative field values before calculation
    if field_T is None or np.any(field_T <= 0):
        print("Warning: Invalid field value(s) (<= 0 or None) provided for g-value calculation.")
        # Return NaN of the same shape as input if it's an array
        if isinstance(field_T, np.ndarray):
            return np.full(field_T.shape, np.nan)
        return np.nan
    return (h * frequency_Hz) / (bohr_magneton * field_T)

def calculate_hyperfine_constant(peak_fields_T, g_value):
    """
    Calculates the hyperfine coupling constant from the spacing between hyperfine peaks.
    A = g * μB * ΔB / h
    
    Args:
        peak_fields_T (np.array): Array of peak positions in Tesla.
        g_value (float): g-value associated with these peaks.
    
    Returns:
        tuple: (A_value_MHz, field_spacing_mT, n_lines)
            A_value_MHz: Hyperfine constant in MHz.
            field_spacing_mT: Average field spacing in mT.
            n_lines: Number of lines used for calculation.
    """
    # Sort peak positions
    sorted_fields = np.sort(peak_fields_T)
    
    if len(sorted_fields) < 2:
        print("Warning: Not enough peaks to calculate hyperfine constant.")
        return np.nan, np.nan, 0
    
    # Calculate spacings between adjacent peaks
    spacings_T = np.diff(sorted_fields)
    
    # Convert to mT for reporting
    spacings_mT = spacings_T * 1000
    
    # Calculate mean spacing
    mean_spacing_T = np.mean(spacings_T)
    mean_spacing_mT = mean_spacing_T * 1000
    
    # Calculate hyperfine constant: A = g * μB * ΔB / h
    # μB = Bohr magneton, h = Planck constant
    A_value_Hz = g_value * bohr_magneton * mean_spacing_T / h
    # Convert to MHz
    A_value_MHz = A_value_Hz / 1e6
    
    return A_value_MHz, mean_spacing_mT, len(sorted_fields) - 1  # n_lines = number of spacings

def analyze_vo_spectrum(magnetic_field_T, derivative):
    """
    Performs a basic analysis for VO(acac)2-like spectra (axial S=1/2, I=7/2).
    Identifies approximate peak positions for parallel and perpendicular components.

    Args:
        magnetic_field_T (np.array): Magnetic field values (Tesla).
        derivative (np.array): First derivative spectrum.

    Returns:
        dict: A dictionary containing analysis results
              {'peaks_indices': indices of detected peaks,
               'g_parallel_approx_field': estimated field for g_parallel center,
               'g_perp_approx_field': estimated field for g_perp center,
               'A_parallel_indices': indices of potential parallel peaks,
               'A_perp_indices': indices of potential perpendicular peaks}
               Returns None if analysis fails.
    """
    try:
        # Find peaks (maxima and minima) in the derivative spectrum
        # Adjust height and distance parameters based on your data's noise/resolution
        # Calculate dynamic height threshold based on derivative range
        deriv_range = np.ptp(derivative) # Peak-to-peak range
        if deriv_range == 0: # Handle flat derivative case
             print("Warning: Derivative range is zero. Cannot determine peak height threshold.")
             height_threshold = None
        else:
            height_threshold = deriv_range * 0.05 # 5% of the range as threshold

        # Find maxima (positive peaks)
        peaks_max_indices, _ = find_peaks(derivative, height=height_threshold, distance=5)
        # Find minima (negative peaks) by inverting the derivative
        peaks_min_indices, _ = find_peaks(-derivative, height=height_threshold, distance=5)

        # Combine and sort all peak indices
        all_peak_indices = np.sort(np.concatenate((peaks_max_indices, peaks_min_indices)))

        if len(all_peak_indices) == 0:
            print("Error: No peaks detected in the derivative spectrum. Check data or peak finding parameters (height, distance).")
            return None
        elif len(all_peak_indices) < 8: # Expect at least 8 lines for V(IV)
            print(f"Warning: Only {len(all_peak_indices)} peaks detected (expected >= 8 for V(IV)). Analysis might be inaccurate.")
            # Proceed with fewer peaks, but results will be less reliable


        # --- Approximate Analysis for VO(acac)2 ---
        # This is a simplified visual estimation. Accurate values require simulation.
        # Assumption: Spectrum spans from low-field parallel lines to high-field parallel lines.
        # Parallel components are usually at the extremes, perpendicular in the center.

        # Estimate center field for g_perpendicular (often near the most intense feature)
        center_region_start_idx = int(len(all_peak_indices) * 0.25)
        center_region_end_idx = int(len(all_peak_indices) * 0.75)
        # Ensure indices are valid even if few peaks are found
        if center_region_start_idx >= center_region_end_idx:
             center_region_start_idx = 0
             center_region_end_idx = len(all_peak_indices)

        central_peak_indices = all_peak_indices[center_region_start_idx:center_region_end_idx]

        if len(central_peak_indices) > 0:
             # Find the index within central_peak_indices corresponding to the largest absolute derivative value
            central_derivative_abs_values = np.abs(derivative[central_peak_indices])
            most_intense_central_peak_local_idx = np.argmax(central_derivative_abs_values)
            # Get the original index from all_peak_indices
            most_intense_central_peak_idx = central_peak_indices[most_intense_central_peak_local_idx]
            g_perp_approx_field = magnetic_field_T[most_intense_central_peak_idx]
            print(f"Estimated g_perp field based on most intense central peak: {g_perp_approx_field*1e4:.2f} G")
        else:
             # Fallback if no central peaks identified (e.g., very few total peaks)
             g_perp_approx_field = np.mean(magnetic_field_T[all_peak_indices])
             print(f"Estimated g_perp field using mean of all detected peaks: {g_perp_approx_field*1e4:.2f} G")


        # Estimate center field for g_parallel (midpoint between outermost detected peaks)
        # These outermost peaks are likely part of the parallel component
        g_parallel_approx_field = (magnetic_field_T[all_peak_indices[0]] + magnetic_field_T[all_peak_indices[-1]]) / 2
        print(f"Estimated g_parallel field based on midpoint of outermost peaks: {g_parallel_approx_field*1e4:.2f} G")

        # Identify potential parallel and perpendicular peaks based on position
        # Parallel lines are expected at the low-field and high-field ends
        # Perpendicular lines are expected in the central region
        # This is a rough assignment for annotation purposes
        num_peaks = len(all_peak_indices)
        # Assign first ~3 and last ~3 peaks as potentially parallel (adjust numbers if needed)
        num_par_each_side = min(3, num_peaks // 2) # Take up to 3 from each side
        parallel_indices = list(all_peak_indices[:num_par_each_side]) + list(all_peak_indices[num_peaks - num_par_each_side:])
        # Assign central peaks as potentially perpendicular
        perp_indices = list(all_peak_indices[num_par_each_side : num_peaks - num_par_each_side])

        # Ensure lists are unique if num_peaks is small causing overlap
        parallel_indices = sorted(list(set(parallel_indices)))
        # Ensure perp_indices doesn't include parallel ones if overlap occurred
        perp_indices = sorted(list(set(perp_indices) - set(parallel_indices)))


        analysis_results = {
            'peaks_indices': all_peak_indices,
            'g_parallel_approx_field': g_parallel_approx_field,
            'g_perp_approx_field': g_perp_approx_field,
            'A_parallel_indices': parallel_indices,
            'A_perp_indices': perp_indices
        }
        return analysis_results

    except Exception as e:
        print(f"An unexpected error occurred during analysis:")
        print(traceback.format_exc())
        return None

def calculate_all_hyperfine_constants(magnetic_field_T, analysis_results, frequency_Hz):
    """
    Calculate hyperfine constants for both parallel and perpendicular components.
    
    Args:
        magnetic_field_T (np.array): Magnetic field values in Tesla.
        analysis_results (dict): Results from analyze_vo_spectrum.
        frequency_Hz (float): Microwave frequency in Hz.
        
    Returns:
        dict: Dictionary containing hyperfine constants and related information.
    """
    results = {}
    
    if not analysis_results:
        print("No analysis results available for hyperfine calculation.")
        return None
    
    # Calculate g-values
    g_parallel = calculate_g_value(analysis_results['g_parallel_approx_field'], frequency_Hz)
    g_perp = calculate_g_value(analysis_results['g_perp_approx_field'], frequency_Hz)
    
    # Store g-values
    results['g_parallel'] = g_parallel
    results['g_perp'] = g_perp
    
    # Calculate A_parallel (using parallel peaks)
    parallel_indices = analysis_results['A_parallel_indices']
    if len(parallel_indices) >= 2:
        parallel_fields = magnetic_field_T[parallel_indices]
        A_parallel_MHz, A_par_spacing_mT, n_par_lines = calculate_hyperfine_constant(parallel_fields, g_parallel)
        
        results['A_parallel_MHz'] = A_parallel_MHz
        results['A_parallel_spacing_mT'] = A_par_spacing_mT
        results['A_parallel_num_lines'] = n_par_lines
        
        print(f"A_parallel calculated: {A_parallel_MHz:.2f} MHz ({A_par_spacing_mT:.2f} mT spacing, {n_par_lines} lines)")
    else:
        print("Not enough parallel peaks to calculate A_parallel.")
        results['A_parallel_MHz'] = np.nan
        results['A_parallel_spacing_mT'] = np.nan
        results['A_parallel_num_lines'] = 0
    
    # Calculate A_perpendicular (using perpendicular peaks)
    perp_indices = analysis_results['A_perp_indices']
    if len(perp_indices) >= 2:
        perp_fields = magnetic_field_T[perp_indices]
        A_perp_MHz, A_perp_spacing_mT, n_perp_lines = calculate_hyperfine_constant(perp_fields, g_perp)
        
        results['A_perp_MHz'] = A_perp_MHz
        results['A_perp_spacing_mT'] = A_perp_spacing_mT
        results['A_perp_num_lines'] = n_perp_lines
        
        print(f"A_perpendicular calculated: {A_perp_MHz:.2f} MHz ({A_perp_spacing_mT:.2f} mT spacing, {n_perp_lines} lines)")
    else:
        print("Not enough perpendicular peaks to calculate A_perpendicular.")
        results['A_perp_MHz'] = np.nan
        results['A_perp_spacing_mT'] = np.nan
        results['A_perp_num_lines'] = 0

    # Calculate isotropic hyperfine coupling constant (aiso)
    if not np.isnan(results['A_parallel_MHz']) and not np.isnan(results['A_perp_MHz']):
        # Aiso = (A_parallel + 2*A_perp)/3
        results['A_isotropic_MHz'] = (results['A_parallel_MHz'] + 2 * results['A_perp_MHz']) / 3
        print(f"Isotropic hyperfine coupling (Aiso): {results['A_isotropic_MHz']:.2f} MHz")
    else:
        results['A_isotropic_MHz'] = np.nan
    
    return results

def plot_epr_spectrum(magnetic_field_T, intensity, derivative, analysis_results, hyperfine_results, frequency_Hz, filepath):
    """
    Plots the EPR absorption and derivative spectra with annotations.

    Args:
        magnetic_field_T (np.array): Magnetic field values (Tesla).
        intensity (np.array): Intensity values.
        derivative (np.array): First derivative values.
        analysis_results (dict): Dictionary from analyze_vo_spectrum. Can be None.
        hyperfine_results (dict): Dictionary with hyperfine constants. Can be None.
        frequency_Hz (float): Microwave frequency in Hz.
        filepath (str): Original filepath, used for title.
    """
    # Convert field back to Gauss for plotting (common convention)
    magnetic_field_G = magnetic_field_T * 1e4

    # --- Plot 1: Absorption Spectrum ---
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.plot(magnetic_field_G, intensity, label='Absorption Signal', color='mediumblue', linewidth=1.5) # Adjusted color/width
    ax1.set_xlabel('Magnetic Field (Gauss)')
    ax1.set_ylabel('Intensity (Arbitrary Units)')
    ax1.set_title(f'EPR Absorption Spectrum\nFile: {filepath}')
    ax1.legend()
    ax1.grid(True, linestyle='--', alpha=0.6) # Adjusted grid style
    plt.tight_layout()
    plt.show(block=False) # Show plot without blocking execution

    # --- Plot 2: Derivative Spectrum ---
    fig2, ax2 = plt.subplots(figsize=(12, 7))
    ax2.plot(magnetic_field_G, derivative, label='First Derivative', color='orangered', linewidth=1.5) # Adjusted color

    # Annotations based on analysis
    # Check if analysis_results is not None before trying to access its keys
    if analysis_results:
        peak_indices = analysis_results.get('peaks_indices', [])
        g_parallel_field_T = analysis_results.get('g_parallel_approx_field')
        g_perp_field_T = analysis_results.get('g_perp_approx_field')
        A_parallel_indices = analysis_results.get('A_parallel_indices', [])
        A_perp_indices = analysis_results.get('A_perp_indices', [])

        if peak_indices.size > 0: # Check if peak_indices is not empty
            peak_fields_G = magnetic_field_G[peak_indices]
            peak_derivs = derivative[peak_indices]
            # Plot markers for all detected peaks
            ax2.plot(peak_fields_G, peak_derivs, 'x', color='black', markersize=7, markeredgewidth=1.5, label='Detected Peaks') # Adjusted marker style

            # Annotate approximate g-values
            if g_perp_field_T:
                g_perp = calculate_g_value(g_perp_field_T, frequency_Hz)
                if not np.isnan(g_perp): # Only plot if g-value is valid
                    g_perp_field_G = g_perp_field_T * 1e4
                    ax2.axvline(g_perp_field_G, color='darkgreen', linestyle='--', linewidth=1.5, label=f'Approx. g⊥ ({g_perp:.4f})') # Adjusted style
                    # Adjust text position dynamically based on plot limits
                    y_range = np.ptp(ax2.get_ylim())
                    y_pos_g_perp = ax2.get_ylim()[1] - 0.1 * y_range
                    ax2.text(g_perp_field_G, y_pos_g_perp, f' g⊥ ≈ {g_perp:.4f}', color='darkgreen', ha='center', weight='bold')


            if g_parallel_field_T:
                 g_parallel = calculate_g_value(g_parallel_field_T, frequency_Hz)
                 if not np.isnan(g_parallel): # Only plot if g-value is valid
                     g_parallel_field_G = g_parallel_field_T * 1e4
                     # Avoid plotting g_parallel line if it's too close to g_perp
                     min_separation_G = 50 # Minimum separation in Gauss to plot distinct lines
                     # Check if g_perp_field_T exists before comparison
                     plot_g_par_line = True
                     if g_perp_field_T:
                         g_perp_field_G_comp = g_perp_field_T * 1e4
                         if abs(g_parallel_field_G - g_perp_field_G_comp) <= min_separation_G:
                             plot_g_par_line = False
                             print(f"Note: g|| annotation ({g_parallel:.4f} at {g_parallel_field_G:.2f} G) overlaps with g⊥ ({g_perp:.4f} at {g_perp_field_G_comp:.2f} G). Skipping g|| line.")


                     if plot_g_par_line:
                         ax2.axvline(g_parallel_field_G, color='darkmagenta', linestyle='--', linewidth=1.5, label=f'Approx. g|| ({g_parallel:.4f})') # Adjusted style
                         y_range = np.ptp(ax2.get_ylim())
                         y_pos_g_par = ax2.get_ylim()[1] - 0.2 * y_range
                         ax2.text(g_parallel_field_G, y_pos_g_par, f' g|| ≈ {g_parallel:.4f}', color='darkmagenta', ha='center', weight='bold')


            # Annotate approximate hyperfine regions (visual aids)
            # Ensure indices are valid before accessing magnetic_field_G or derivative
            valid_A_par_indices = [idx for idx in A_parallel_indices if idx < len(magnetic_field_G)]
            if valid_A_par_indices: # Check if list is not empty after validation
                 parallel_fields_G = magnetic_field_G[valid_A_par_indices]
                 if len(parallel_fields_G) > 0: # Ensure there are fields to process
                     min_par_field = np.min(parallel_fields_G)
                     max_par_field = np.max(parallel_fields_G)
                     # Find corresponding derivative values for arrow vertical placement (use median for robustness)
                     median_par_deriv = np.median(derivative[valid_A_par_indices])
                     y_range = np.ptp(ax2.get_ylim())
                     y_pos_par_arrow = median_par_deriv + 0.1 * y_range # Place above median peak

                     # Draw arrows pointing inwards from the extremes
                     ax2.annotate('A|| region', xy=(min_par_field, derivative[valid_A_par_indices[0]]), xytext=(min_par_field - 150, y_pos_par_arrow),
                                  arrowprops=dict(arrowstyle='->', color='darkblue', lw=1.5), color='darkblue', ha='right', va='center')
                     ax2.annotate('A|| region', xy=(max_par_field, derivative[valid_A_par_indices[-1]]), xytext=(max_par_field + 150, y_pos_par_arrow),
                                  arrowprops=dict(arrowstyle='->', color='darkblue', lw=1.5), color='darkblue', ha='left', va='center')


            valid_A_perp_indices = [idx for idx in A_perp_indices if idx < len(magnetic_field_G)]
            if valid_A_perp_indices: # Check if list is not empty after validation
                 perp_fields_G = magnetic_field_G[valid_A_perp_indices]
                 if len(perp_fields_G) > 0: # Ensure there are fields to process
                     min_perp_field = np.min(perp_fields_G)
                     max_perp_field = np.max(perp_fields_G)
                     # Find derivative value near the center for annotation placement (use median)
                     median_perp_deriv = np.median(derivative[valid_A_perp_indices])
                     y_range = np.ptp(ax2.get_ylim())
                     y_pos_perp_bracket = median_perp_deriv - 0.1 * y_range # Place below median peak

                     # Draw bracket indicating the span of perpendicular features
                     ax2.annotate('', xy=(min_perp_field, y_pos_perp_bracket), xytext=(max_perp_field, y_pos_perp_bracket),
                                  arrowprops=dict(arrowstyle='<->', color='purple', lw=1.5))
                     ax2.text((min_perp_field + max_perp_field)/2, y_pos_perp_bracket - 0.05 * y_range, 'A⊥ region',
                              color='purple', ha='center', va='top', weight='bold')

        else:
            print("No peaks were detected, skipping derivative plot annotations.")

    else:
        print("Analysis results were None, skipping derivative plot annotations.")

    # Add hyperfine constants to the plot if available
    if hyperfine_results:
        # Create text for hyperfine parameters
        hyperfine_text = "EPR Parameters:\n"
        
        # Add g-values
        if 'g_parallel' in hyperfine_results and not np.isnan(hyperfine_results['g_parallel']):
            hyperfine_text += f"g_|| = {hyperfine_results['g_parallel']:.4f}\n"
        if 'g_perp' in hyperfine_results and not np.isnan(hyperfine_results['g_perp']):
            hyperfine_text += f"g_⊥ = {hyperfine_results['g_perp']:.4f}\n"
        
        # Add A values
        if 'A_parallel_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_parallel_MHz']):
            hyperfine_text += f"A_|| = {hyperfine_results['A_parallel_MHz']:.2f} MHz\n"
        if 'A_perp_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_perp_MHz']):
            hyperfine_text += f"A_⊥ = {hyperfine_results['A_perp_MHz']:.2f} MHz\n"
        if 'A_isotropic_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_isotropic_MHz']):
            hyperfine_text += f"A_iso = {hyperfine_results['A_isotropic_MHz']:.2f} MHz"
        
        # Position text in upper left corner of the plot
        ax2.text(0.02, 0.98, hyperfine_text, transform=ax2.transAxes, fontsize=10,
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'),
                verticalalignment='top', horizontalalignment='left')

    ax2.set_xlabel('Magnetic Field (Gauss)')
    ax2.set_ylabel('d(Intensity)/d(Field) (Arbitrary Units)')
    ax2.set_title(f'EPR First Derivative Spectrum (VO(acac)₂ Analysis)\nFrequency: {MICROWAVE_FREQUENCY_GHZ} GHz')
    # Improve legend placement
    ax2.legend(loc='best', fontsize='small', frameon=True, framealpha=0.8)
    ax2.grid(True, linestyle='--', alpha=0.6) # Adjusted grid style
    plt.tight_layout() # Adjust layout to prevent labels overlapping
    plt.show() # Show the second plot and block until closed

def summarize_epr_parameters(hyperfine_results):
    """
    Print a summary of the calculated EPR parameters.
    
    Args:
        hyperfine_results (dict): Dictionary containing g-values and hyperfine constants.
        
    Returns:
        None: Prints information to console.
    """
    if not hyperfine_results:
        print("No EPR parameters available to summarize.")
        return
    
    print("\n" + "="*60)
    print("VANADIUM EPR PARAMETER SUMMARY")
    print("="*60)
    
    # Report g-values
    print("G-VALUES:")
    if 'g_parallel' in hyperfine_results and not np.isnan(hyperfine_results['g_parallel']):
        print(f"  g_|| = {hyperfine_results['g_parallel']:.4f}")
    else:
        print("  g_|| = Not determined")
        
    if 'g_perp' in hyperfine_results and not np.isnan(hyperfine_results['g_perp']):
        print(f"  g_⊥ = {hyperfine_results['g_perp']:.4f}")
    else:
        print("  g_⊥ = Not determined")
    
    # Calculate average g value: g_avg = (g_parallel + 2*g_perp)/3
    if ('g_parallel' in hyperfine_results and not np.isnan(hyperfine_results['g_parallel']) and
        'g_perp' in hyperfine_results and not np.isnan(hyperfine_results['g_perp'])):
        g_avg = (hyperfine_results['g_parallel'] + 2 * hyperfine_results['g_perp']) / 3
        print(f"  g_avg = {g_avg:.4f}  [calculated as (g_|| + 2g_⊥)/3]")
    
    print("\nHYPERFINE COUPLING CONSTANTS:")
    # Report A values
    if 'A_parallel_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_parallel_MHz']):
        print(f"  A_|| = {hyperfine_results['A_parallel_MHz']:.2f} MHz")
        if 'A_parallel_spacing_mT' in hyperfine_results:
            print(f"        = {hyperfine_results['A_parallel_spacing_mT']:.2f} mT spacing")
        if 'A_parallel_num_lines' in hyperfine_results:
            print(f"        (Based on {hyperfine_results['A_parallel_num_lines']} line spacings)")
    else:
        print("  A_|| = Not determined")
    
    if 'A_perp_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_perp_MHz']):
        print(f"  A_⊥ = {hyperfine_results['A_perp_MHz']:.2f} MHz")
        if 'A_perp_spacing_mT' in hyperfine_results:
            print(f"        = {hyperfine_results['A_perp_spacing_mT']:.2f} mT spacing")
        if 'A_perp_num_lines' in hyperfine_results:
            print(f"        (Based on {hyperfine_results['A_perp_num_lines']} line spacings)")
    else:
        print("  A_⊥ = Not determined")
    
    if 'A_isotropic_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_isotropic_MHz']):
        print(f"  A_iso = {hyperfine_results['A_isotropic_MHz']:.2f} MHz  [calculated as (A_|| + 2A_⊥)/3]")
    else:
        print("  A_iso = Not determined")
    
    print("\nINTERPRETATION:")
    # Provide basic interpretation for V(IV) spectra
    print("  • This analysis assumes a V(IV) species with S=1/2 and I=7/2 (51V nucleus).")
    print("  • Typical values for VO(acac)₂: g_|| ≈ 1.94, g_⊥ ≈ 1.98")
    print("  • Typical values for VO(acac)₂: A_|| ≈ 170-180 MHz, A_⊥ ≈ 60-70 MHz")
    
    # Assess quality of analysis based on expected values
    if ('g_parallel' in hyperfine_results and not np.isnan(hyperfine_results['g_parallel']) and
        'g_perp' in hyperfine_results and not np.isnan(hyperfine_results['g_perp'])):
        
        # Check if g-values are in expected ranges for VO complexes
        g_par_in_range = 1.92 <= hyperfine_results['g_parallel'] <= 1.96
        g_perp_in_range = 1.96 <= hyperfine_results['g_perp'] <= 2.00
        
        if g_par_in_range and g_perp_in_range:
            print("\n  ✓ The g-values are consistent with VO(IV) complexes.")
        else:
            print("\n  ⚠ Some g-values appear outside the typical range for VO(IV) complexes.")
            if not g_par_in_range:
                print(f"    - g_|| = {hyperfine_results['g_parallel']:.4f} (typical range: 1.92-1.96)")
            if not g_perp_in_range:
                print(f"    - g_⊥ = {hyperfine_results['g_perp']:.4f} (typical range: 1.96-2.00)")
    
    if ('A_parallel_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_parallel_MHz']) and
        'A_perp_MHz' in hyperfine_results and not np.isnan(hyperfine_results['A_perp_MHz'])):
        
        # Check if A-values are in expected ranges
        A_par_in_range = 160 <= hyperfine_results['A_parallel_MHz'] <= 190
        A_perp_in_range = 50 <= hyperfine_results['A_perp_MHz'] <= 80
        
        if A_par_in_range and A_perp_in_range:
            print("  ✓ The hyperfine constants are consistent with VO(IV) complexes.")
        else:
            print("  ⚠ Some hyperfine constants appear outside the typical range for VO(IV) complexes.")
            if not A_par_in_range:
                print(f"    - A_|| = {hyperfine_results['A_parallel_MHz']:.2f} MHz (typical range: 160-190 MHz)")
            if not A_perp_in_range:
                print(f"    - A_⊥ = {hyperfine_results['A_perp_MHz']:.2f} MHz (typical range: 50-80 MHz)")
    
    print("\nNOTE: This is an automated analysis and should be validated by manual inspection.")
    print("      For publication-quality results, simulation and fitting is recommended.")
    print("="*60)
    
    
    
# --- Main Execution ---
def main():
    """Execute the full EPR analysis workflow."""
    try:
        # Convert microwave frequency to Hz
        frequency_Hz = MICROWAVE_FREQUENCY_GHZ * 1e9
        print(f"Using microwave frequency: {MICROWAVE_FREQUENCY_GHZ} GHz ({frequency_Hz/1e9:.4f} GHz)")
        
        # Read the EPR data
        print(f"\nReading EPR data from: {FILE_PATH}")
        magnetic_field_T, intensity = read_epr_asc(FILE_PATH)
        
        if magnetic_field_T is None or intensity is None:
            print("Failed to read EPR data. Please check the file path and format.")
            return
            
        print(f"Successfully read {len(magnetic_field_T)} data points.")
        
        # Calculate the first derivative
        print("\nCalculating first derivative...")
        derivative = calculate_derivative(magnetic_field_T, intensity)
        
        # Analyze the spectrum
        print("\nAnalyzing VO spectrum...")
        analysis_results = analyze_vo_spectrum(magnetic_field_T, derivative)
        
        # Calculate hyperfine constants
        print("\nCalculating hyperfine parameters...")
        hyperfine_results = calculate_all_hyperfine_constants(magnetic_field_T, analysis_results, frequency_Hz)
        
        # Plot the results
        print("\nPlotting spectra...")
        plot_epr_spectrum(magnetic_field_T, intensity, derivative, analysis_results, 
                          hyperfine_results, frequency_Hz, FILE_PATH)
        
        # Summarize the results
        summarize_epr_parameters(hyperfine_results)
        
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        print(traceback.format_exc())

if __name__ == "__main__":
    main()
