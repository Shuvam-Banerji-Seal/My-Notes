import numpy as np
import random
import time
import math
import argparse
from datetime import datetime
import json
import os
import matplotlib.pyplot as plt

# --- Command Line Arguments ---
def parse_arguments():
    parser = argparse.ArgumentParser(description='O2 Concentration vs QY Simulation')
    
    # Core simulation parameters
    parser.add_argument('--grid-size', type=int, default=100, help='Size of the simulation grid')
    parser.add_argument('--core-radius', type=float, default=15, help='Characteristic radius of the core region')
    parser.add_argument('--surface-thickness', type=float, default=5, help='Thickness of the surface layer')
    parser.add_argument('--num-ru1', type=int, default=30, help='Number of Ru(1) surface complexes')
    parser.add_argument('--num-ru2', type=int, default=30, help='Number of Ru(2) core complexes')
    parser.add_argument('--min-o2', type=int, default=10, help='Minimum number of oxygen molecules')
    parser.add_argument('--max-o2', type=int, default=200, help='Maximum number of oxygen molecules')
    parser.add_argument('--o2-steps', type=int, default=10, help='Number of O2 concentration steps')
    parser.add_argument('--steps', type=int, default=600, help='Number of simulation time steps')
    
    # Physical model parameters
    parser.add_argument('--excited-lifetime', type=int, default=30, help='Excited state lifetime in time steps')
    parser.add_argument('--quenching-radius', type=float, default=1.8, help='Distance for quenching')
    parser.add_argument('--o2-prob-max', type=float, default=0.98, help='Maximum O2 movement probability')
    parser.add_argument('--o2-prob-min', type=float, default=0.10, help='Minimum O2 movement probability')
    parser.add_argument('--density-steepness', type=float, default=0.3, help='Steepness of density gradient')
    parser.add_argument('--excitation-prob', type=float, default=1.0, help='Probability of excitation per time step')
    
    # Output options
    parser.add_argument('--save-path', type=str, default='simulation_results', help='Path to save results')
    
    return parser.parse_args()

# --- Classes ---
class RutheniumComplex:
    """ Represents a Ruthenium complex molecule with enhanced tracking capabilities """
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # 'Ru1' (surface) or 'Ru2' (core)
        self.state = 'ground'  # 'ground' or 'excited'
        self.excited_timer = 0
        self.emission_count = 0
        self.quenched_count = 0
        self.total_excitations = 0
        
        # Enhanced tracking
        self.lifetime_history = []  # Track excited state durations
        self.quencher_distances = []  # Track distances to quenchers when quenched
        
    def excite(self, excitation_prob=1.0, lifetime=30):
        """Excite the complex with given probability and lifetime"""
        if self.state == 'ground' and random.random() < excitation_prob:
            self.state = 'excited'
            self.excited_timer = lifetime
            self.total_excitations += 1

    def step(self):
        """Update the complex state for one time step"""
        if self.state == 'excited':
            self.excited_timer -= 1
            if self.excited_timer <= 0:
                self.emit()

    def quench(self, quencher_distance=None):
        """Quench the complex and record quenching event data"""
        if self.state == 'excited':
            # Calculate lifetime that was achieved before quenching
            achieved_lifetime = self.excited_timer
            self.lifetime_history.append(achieved_lifetime)
            
            # Record quencher distance if provided
            if quencher_distance is not None:
                self.quencher_distances.append(quencher_distance)
                
            # Reset state
            self.state = 'ground'
            self.excited_timer = 0
            self.quenched_count += 1

    def emit(self):
        """Emit light and record emission event"""
        if self.state == 'excited':
            # Calculate full lifetime that was achieved
            achieved_lifetime = self.excited_timer
            self.lifetime_history.append(achieved_lifetime)
            
            # Reset state
            self.state = 'ground'
            self.excited_timer = 0
            self.emission_count += 1

    def get_simulated_qy(self):
        """Calculate quantum yield from recorded events"""
        total_events = self.emission_count + self.quenched_count
        return self.emission_count / total_events if total_events > 0 else 0

class OxygenMolecule:
    """ Represents an Oxygen molecule (quencher) with enhanced tracking. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.quench_count = 0
        
    def move(self, grid_size, core_center, core_radius, density_steepness, prob_min, prob_max):
        """ Moves the oxygen molecule with density-dependent probability. """
        # Calculate density and movement probability
        density = get_polymer_density(self.x, self.y, core_center, core_radius, density_steepness)
        move_prob = prob_max - density * (prob_max - prob_min)
        move_prob = max(prob_min, min(prob_max, move_prob))  # Clamp probability

        if random.random() < move_prob:
            # Move one step in a random direction
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            # Apply boundary conditions (stay within grid)
            new_x = max(0, min(grid_size - 1, self.x + dx))
            new_y = max(0, min(grid_size - 1, self.y + dy))
            self.x, self.y = new_x, new_y
    
    def record_quench(self):
        """Record a quenching event by this O2 molecule"""
        self.quench_count += 1

# --- Helper Functions ---
def get_polymer_density(x, y, center, radius, steepness):
    """ Calculates polymer density using a sigmoid-like function. """
    dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
    # Sigmoid function centered around 'radius'
    exponent = steepness * (dist - radius)
    # Clamp exponent to prevent overflow/underflow
    exponent = max(-700, min(700, exponent))
    try:
        density = 1 / (1 + math.exp(exponent))
    except OverflowError:
        # If exponent too large, density is effectively 0
        density = 0.0
    return density

def is_in_core_region(x, y, center, radius):
    """ Checks if coordinates are within the core radius. """
    return (x - center[0])**2 + (y - center[1])**2 < radius**2

def place_complexes(num, type, grid_size, core_center, core_radius, surface_thickness):
    """ Places Ru complexes in appropriate regions. """
    complexes = []
    attempts = 0
    max_attempts = num * 300
    surface_outer_radius = core_radius + surface_thickness

    while len(complexes) < num and attempts < max_attempts:
        attempts += 1
        x = random.uniform(0, grid_size - 1)
        y = random.uniform(0, grid_size - 1)
        in_core_flag = is_in_core_region(x, y, core_center, core_radius)
        dist_from_center = math.sqrt((x - core_center[0])**2 + (y - core_center[1])**2)

        if type == 'Ru1' and not in_core_flag and dist_from_center < surface_outer_radius:
            complexes.append(RutheniumComplex(x, y, type))
        elif type == 'Ru2' and in_core_flag:
            complexes.append(RutheniumComplex(x, y, type))

    if len(complexes) < num:
        print(f"Warning: Could only place {len(complexes)} of {num} desired {type} complexes.")
    return complexes

def place_oxygen_molecules(num_o2, grid_size, core_center, core_radius, density_steepness):
    """Place O2 molecules with distribution weighted by polymer density"""
    o2_molecules = []
    attempts = 0
    max_attempts = num_o2 * 10
    
    while len(o2_molecules) < num_o2 and attempts < max_attempts:
        attempts += 1
        x = random.uniform(0, grid_size - 1)
        y = random.uniform(0, grid_size - 1)
        
        # Calculate probability based on density
        density = get_polymer_density(x, y, core_center, core_radius, density_steepness)
        if random.random() < density:
            o2_molecules.append(OxygenMolecule(x, y))
    
    return o2_molecules

def save_results(o2_counts, ru1_qy_values, ru2_qy_values, args, save_path):
    """Save results to CSV and JSON files"""
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create results dictionary
    results = {
        "parameters": vars(args),
        "timestamp": datetime.now().isoformat(),
        "data": {
            "o2_counts": o2_counts,
            "ru1_qy_values": ru1_qy_values,
            "ru2_qy_values": ru2_qy_values
        }
    }
    
    # Save to JSON
    json_filename = os.path.join(save_path, f"o2_vs_qy_{timestamp}.json")
    with open(json_filename, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Also save as CSV for easy importing into other software
    csv_filename = os.path.join(save_path, f"o2_vs_qy_{timestamp}.csv")
    with open(csv_filename, 'w') as f:
        f.write("O2_Count,Ru1_QY,Ru2_QY\n")
        for i in range(len(o2_counts)):
            f.write(f"{o2_counts[i]},{ru1_qy_values[i]},{ru2_qy_values[i]}\n")
    
    print(f"Results saved to: {json_filename} and {csv_filename}")
    return json_filename, csv_filename

def plot_results(o2_counts, ru1_qy_values, ru2_qy_values, save_path):
    """Create visualization of results"""
    plt.figure(figsize=(12, 8))
    
    # Plot QY vs O2 concentration
    plt.plot(o2_counts, ru1_qy_values, 'o-', color='orangered', label='Ru1 (Surface)')
    plt.plot(o2_counts, ru2_qy_values, 's-', color='deepskyblue', label='Ru2 (Core)')
    
    plt.xlabel('O₂ Concentration (Number of Molecules)', fontsize=14)
    plt.ylabel('Quantum Yield', fontsize=14)
    plt.title('Ruthenium Complex Quantum Yield vs O₂ Concentration', fontsize=16)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=12)
    
    # Add text annotation explaining the relationship
    y_pos = min(min(ru1_qy_values), min(ru2_qy_values))
    plt.annotate(
        "Quantum yield decreases with increasing O₂ concentration\n"
        "due to increased quenching events",
        xy=(0.5, 0.02), xycoords='axes fraction',
        ha='center', fontsize=12, bbox=dict(boxstyle="round,pad=0.5", fc="lightyellow", alpha=0.8)
    )
    
    plt.tight_layout()
    
    # Save figure
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_path, f"o2_vs_qy_plot_{timestamp}.png")
    plt.savefig(filename, dpi=300)
    print(f"Plot saved as: {filename}")
    
    return filename

def run_single_simulation(args, num_o2):
    """Run a single simulation with specified O2 count"""
    # Set up grid and calculate centers
    grid_size = args.grid_size
    core_center = (grid_size / 2, grid_size / 2)
    
    # Place Ru complexes (only need to do this once)
    ru1_complexes = place_complexes(args.num_ru1, 'Ru1', grid_size, core_center, 
                                   args.core_radius, args.surface_thickness)
    ru2_complexes = place_complexes(args.num_ru2, 'Ru2', grid_size, core_center, 
                                   args.core_radius, args.surface_thickness)
    
    # Place O2 molecules
    o2_molecules = place_oxygen_molecules(num_o2, grid_size, core_center, 
                                         args.core_radius, args.density_steepness)
    
    # Run simulation without visualization
    for step in range(args.steps):
        # 1. Excite complexes
        for ru in ru1_complexes + ru2_complexes:
            ru.excite(args.excitation_prob, args.excited_lifetime)

        # 2. Move Oxygen
        for o2 in o2_molecules:
            o2.move(grid_size, core_center, args.core_radius, args.density_steepness, 
                   args.o2_prob_min, args.o2_prob_max)

        # 3. Check for Quenching
        for ru in ru1_complexes + ru2_complexes:
            if ru.state == 'excited':
                for o2 in o2_molecules:
                    dist_sq = (ru.x - o2.x)**2 + (ru.y - o2.y)**2
                    if dist_sq < args.quenching_radius ** 2:
                        ru.quench(math.sqrt(dist_sq))
                        o2.record_quench()
                        break  # Quenched

        # 4. Ru complexes evolve (timer/emission)
        for ru in ru1_complexes + ru2_complexes:
            ru.step()
    
    # Calculate QY values
    ru1_emissions = sum(c.emission_count for c in ru1_complexes)
    ru1_quenched = sum(c.quenched_count for c in ru1_complexes)
    ru1_total_events = ru1_emissions + ru1_quenched
    simulated_qy_ru1 = ru1_emissions / ru1_total_events if ru1_total_events > 0 else 0
    
    ru2_emissions = sum(c.emission_count for c in ru2_complexes)
    ru2_quenched = sum(c.quenched_count for c in ru2_complexes)
    ru2_total_events = ru2_emissions + ru2_quenched
    simulated_qy_ru2 = ru2_emissions / ru2_total_events if ru2_total_events > 0 else 0
    
    return simulated_qy_ru1, simulated_qy_ru2, len(o2_molecules)

# --- Main Function ---
def run_o2_concentration_study(args):
    """Run simulations with varying O2 concentrations"""
    print(f"\nStarting O2 concentration vs QY study ({args.min_o2} to {args.max_o2} O2 molecules)")
    print("=" * 50)
    
    # Generate O2 counts to test
    o2_counts = np.linspace(args.min_o2, args.max_o2, args.o2_steps, dtype=int)
    
    # Arrays to store results
    actual_o2_counts = []
    ru1_qy_values = []
    ru2_qy_values = []
    
    # Run simulations for each O2 concentration
    total_start_time = time.time()
    
    for i, num_o2 in enumerate(o2_counts):
        print(f"\nRunning simulation {i+1}/{len(o2_counts)}: {num_o2} O2 molecules")
        start_time = time.time()
        
        # Run simulation and collect results
        ru1_qy, ru2_qy, actual_o2 = run_single_simulation(args, num_o2)
        
        # Store results
        actual_o2_counts.append(actual_o2)
        ru1_qy_values.append(ru1_qy)
        ru2_qy_values.append(ru2_qy)
        
        # Print progress
        elapsed = time.time() - start_time
        print(f"  Completed in {elapsed:.2f} seconds")
        print(f"  Results: Ru1 QY = {ru1_qy:.4f}, Ru2 QY = {ru2_qy:.4f}, Actual O2 = {actual_o2}")
    
    # Save results
    json_file, csv_file = save_results(actual_o2_counts, ru1_qy_values, ru2_qy_values, args, args.save_path)
    
    # Plot results
    plot_file = plot_results(actual_o2_counts, ru1_qy_values, ru2_qy_values, args.save_path)
    
    # Print summary
    total_time = time.time() - total_start_time
    print("\nStudy Complete!")
    print(f"Total runtime: {total_time:.2f} seconds")
    print(f"Results saved to: {json_file}")
    print(f"CSV data saved to: {csv_file}")
    print(f"Plot saved to: {plot_file}")
    
    return actual_o2_counts, ru1_qy_values, ru2_qy_values

# --- Main Entry Point ---
if __name__ == "__main__":
    args = parse_arguments()
    print("O2 Concentration vs Quantum Yield Study")
    print("=" * 40)
    print(f"Grid Size: {args.grid_size}x{args.grid_size}")
    print(f"Core Radius: {args.core_radius}, Surface Thickness: {args.surface_thickness}")
    print(f"Ru1: {args.num_ru1}, Ru2: {args.num_ru2}")
    print(f"O2 Range: {args.min_o2} to {args.max_o2} in {args.o2_steps} steps")
    print(f"Simulation Steps: {args.steps}")
    
    # Create save directory if needed
    os.makedirs(args.save_path, exist_ok=True)
    
    # Run the concentration study
    o2_counts, ru1_qy_values, ru2_qy_values = run_o2_concentration_study(args)