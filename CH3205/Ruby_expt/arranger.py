#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create the main directory structure for the lab data."""
    directories = [
        'data',
        'data/nmr',
        'data/mass_spec',
        'data/cv',
        'data/pl',
        'data/uv_vis',
        'scripts',
        'figures',
        'figures/cv',
        'figures/pl',
        'figures/uv_vis',
        'figures/nmr'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def move_files(base_path):
    """Move files to their appropriate directories."""
    # Move Python scripts
    for script in ['cv_plot.py', 'pl_plot.py', 'uv_vis.py', 'uv_vis_tottal.py']:
        if os.path.exists(script):
            shutil.move(script, f'scripts/{script}')

    # Move NMR files
    nmr_files = Path('NMR').glob('*')
    for file in nmr_files:
        shutil.move(str(file), f'data/nmr/{file.name}')
    if os.path.exists('1H-NMR_CH3205 FINAL.pdf'):
        shutil.move('1H-NMR_CH3205 FINAL.pdf', 'data/nmr/1H-NMR_CH3205 FINAL.pdf')

    # Move Mass Spec files
    mass_files = Path('Mass_spectra').glob('*')
    for file in mass_files:
        shutil.move(str(file), f'data/mass_spec/{file.name}')
    if os.path.exists('MASS-CH3205.pdf'):
        shutil.move('MASS-CH3205.pdf', 'data/mass_spec/MASS-CH3205.pdf')

    # Move CV files
    cv_files = Path('CV').glob('*')
    for file in cv_files:
        shutil.move(str(file), f'data/cv/{file.name}')
    for csv_file in ['Ru_Anodic_vs_Fc.csv', 'Ru_Cathodic_vs_Fc.csv']:
        if os.path.exists(csv_file):
            shutil.move(csv_file, f'data/cv/{csv_file}')

    # Move PL data
    pl_files = Path('PL_data').glob('*')
    for file in pl_files:
        shutil.move(str(file), f'data/pl/{file.name}')

    # Move UV-Vis data
    uv_files = Path('UV-Vis_data').glob('*')
    for file in uv_files:
        shutil.move(str(file), f'data/uv_vis/{file.name}')

    # Move figures to appropriate directories
    figure_mappings = {
        'cv': ['cv_comparison_all_peaks.png', 'cv_comparison.png', 'cv_standardized.png', 
               'cv_standardized_with_peaks.png', 'cyclic_voltammetry_plot.png'],
        'pl': ['pl_22ms012.png', 'pl_22ms016.png'],
        'uv_vis': ['uv_spectrum_print.pdf', 'uv_vis_22ms076.png'],
        'nmr': ['average_spectrum.png', 'overlaid_spectra.png']
    }

    for category, files in figure_mappings.items():
        for file in files:
            if os.path.exists(file):
                shutil.move(file, f'figures/{category}/{file}')

def cleanup_empty_dirs():
    """Remove empty directories after moving files."""
    dirs_to_remove = ['NMR', 'Mass_spectra', 'CV', 'PL_data', 'UV-Vis_data']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                os.rmdir(dir_name)
            except OSError:
                print(f"Warning: {dir_name} not empty or already removed")

def main():
    create_directory_structure()
    move_files(os.getcwd())
    cleanup_empty_dirs()
    print("Lab directory reorganization complete!")

if __name__ == "__main__":
    main()