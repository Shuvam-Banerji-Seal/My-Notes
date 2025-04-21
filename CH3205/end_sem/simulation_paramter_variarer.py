import numpy as np
import random
import time
import math
import csv # Added for CSV output
import itertools # Added for parameter combinations
import os # Added to manage file paths

# --- Simulation Parameters (Defaults - some will be overridden by sweep) ---
GRID_SIZE = 50
CORE_RADIUS = 15
SURFACE_THICKNESS = 5
NUM_RU1 = 30
NUM_RU2 = 30
NUM_O2 = 180 # Will be varied
SIMULATION_STEPS = 500 # Reduced for faster batch runs, increase if needed
EXCITED_LIFETIME = 30 # Will be varied
QUENCHING_RADIUS = 1.8
QUENCHING_RADIUS_SQ = QUENCHING_RADIUS**2
O2_MOVE_PROB_MAX = 0.98
O2_MOVE_PROB_MIN = 0.10 # Will be varied
DENSITY_STEEPNESS = 0.3 # Will be varied

# --- Parameter Sweep Configuration ---
# Define the parameters and ranges to vary
param_sweep_config = {
    'NUM_O2': [100, 180, 250],
    'DENSITY_STEEPNESS': [0.2, 0.3, 0.5],
    'O2_MOVE_PROB_MIN': [0.05, 0.10, 0.15],
    'EXCITED_LIFETIME': [20, 30, 40]
    # Add other parameters here if desired, e.g., 'CORE_RADIUS': [10, 15, 20]
}

# --- File Output Configuration ---
RESULTS_FILENAME = 'simulation_results.csv'

# --- Disable Visualization for Batch Runs ---
VISUALIZE = False # Keep False for parameter sweeps

# --- Classes (RutheniumComplex, OxygenMolecule) ---
# Unchanged from the previous version - keeping them internal for clarity
class RutheniumComplex:
    """ Represents a Ruthenium complex molecule. """
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # 'Ru1' (surface) or 'Ru2' (core)
        self.state = 'ground'
        self.excited_timer = 0
        self.emission_count = 0
        self.quenched_count = 0
        # Removed total_excitations as it's not directly used in final QY calc

    def excite(self, lifetime):
        if self.state == 'ground':
            self.state = 'excited'
            self.excited_timer = lifetime # Use passed lifetime

    def step(self):
        if self.state == 'excited':
            self.excited_timer -= 1
            if self.excited_timer <= 0:
                self.emit()

    def quench(self):
        if self.state == 'excited':
            self.state = 'ground'
            self.excited_timer = 0
            self.quenched_count += 1

    def emit(self):
        if self.state == 'excited':
            self.state = 'ground'
            self.excited_timer = 0
            self.emission_count += 1

    def get_simulated_qy(self):
        total_events = self.emission_count + self.quenched_count
        return self.emission_count / total_events if total_events > 0 else 0

class OxygenMolecule:
    """ Represents an Oxygen molecule (quencher). """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, grid_size, core_center, core_radius, density_steepness, prob_min, prob_max):
        """ Moves the oxygen molecule randomly, hindered by polymer density. """
        density = get_polymer_density(self.x, self.y, core_center, core_radius, density_steepness)
        move_prob = prob_max - density * (prob_max - prob_min)
        move_prob = max(prob_min, min(prob_max, move_prob))

        if random.random() < move_prob:
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])
            new_x = max(0, min(grid_size - 1, self.x + dx))
            new_y = max(0, min(grid_size - 1, self.y + dy))
            self.x = new_x
            self.y = new_y

# --- Helper Functions (get_polymer_density, is_in_core_region, place_complexes) ---
# Unchanged from the previous version
def get_polymer_density(x, y, center, radius, steepness):
    """ Calculates a simulated polymer density based on distance from the center. """
    dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
    # Sigmoid function centered around 'radius'
    # Added small epsilon to prevent potential math domain error if dist exactly equals radius and steepness is high
    exponent = steepness * (dist - radius)
    # Clamp exponent to prevent overflow/underflow with large steepness/distance
    exponent = max(-700, min(700, exponent))
    try:
        density = 1 / (1 + math.exp(exponent))
    except OverflowError:
        # If exp(exponent) is too large, density is effectively 0
        density = 0.0
    return density

def is_in_core_region(x, y, center, radius):
    """ Checks if coordinates (x, y) are within the nominal core radius (for placement). """
    return (x - center[0])**2 + (y - center[1])**2 < radius**2

def place_complexes(num, type, grid_size, core_center, core_radius, surface_thickness):
    """ Places Ru complexes either in the core region or near the surface region. """
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
        print(f"  Warning: Could only place {len(complexes)} of {num} desired {type} complexes.")
    return complexes

# --- Simulation Function ---
def run_simulation(params):
    """ Runs a single simulation with the given parameters. """
    # Unpack parameters, using defaults if not provided in sweep
    num_o2 = params.get('NUM_O2', NUM_O2)
    density_steepness = params.get('DENSITY_STEEPNESS', DENSITY_STEEPNESS)
    o2_move_prob_min = params.get('O2_MOVE_PROB_MIN', O2_MOVE_PROB_MIN)
    excited_lifetime = params.get('EXCITED_LIFETIME', EXCITED_LIFETIME)
    # Use other defaults
    grid_size = GRID_SIZE
    core_radius = CORE_RADIUS
    surface_thickness = SURFACE_THICKNESS
    num_ru1 = NUM_RU1
    num_ru2 = NUM_RU2
    simulation_steps = SIMULATION_STEPS
    quenching_radius_sq = QUENCHING_RADIUS_SQ
    o2_move_prob_max = O2_MOVE_PROB_MAX

    core_center = (grid_size / 2, grid_size / 2)

    # Setup simulation environment for this run
    ru1_complexes = place_complexes(num_ru1, 'Ru1', grid_size, core_center, core_radius, surface_thickness)
    ru2_complexes = place_complexes(num_ru2, 'Ru2', grid_size, core_center, core_radius, surface_thickness)
    all_complexes = ru1_complexes + ru2_complexes

    o2_molecules = []
    attempts = 0
    max_attempts = num_o2 * 100
    while len(o2_molecules) < num_o2 and attempts < max_attempts:
        attempts += 1
        x = random.uniform(0, grid_size - 1)
        y = random.uniform(0, grid_size - 1)
        if get_polymer_density(x, y, core_center, core_radius, density_steepness) < 0.3:
             o2_molecules.append(OxygenMolecule(x, y))
    # Add warning if placement failed significantly
    if len(o2_molecules) < num_o2 * 0.8: # If less than 80% placed
        print(f"  Warning: Could only place {len(o2_molecules)} of {num_o2} O2 molecules initially for this run.")


    # Check if complexes were placed
    if not ru1_complexes or not ru2_complexes:
        print("  Error: Failed to place Ru complexes. Skipping this run.")
        return None # Indicate failure

    # Simulation Loop for this run
    for step in range(simulation_steps):
        for ru in all_complexes: ru.excite(excited_lifetime) # Pass lifetime
        for o2 in o2_molecules: o2.move(grid_size, core_center, core_radius, density_steepness, o2_move_prob_min, o2_move_prob_max)
        for ru in all_complexes:
            if ru.state == 'excited':
                for o2 in o2_molecules:
                    dist_sq = (ru.x - o2.x)**2 + (ru.y - o2.y)**2
                    if dist_sq < quenching_radius_sq:
                        ru.quench()
                        break
        for ru in all_complexes: ru.step()

    # Calculate results for this run
    ru1_emissions = sum(c.emission_count for c in ru1_complexes)
    ru1_quenched = sum(c.quenched_count for c in ru1_complexes)
    ru1_total_events = ru1_emissions + ru1_quenched
    simulated_qy_ru1 = ru1_emissions / ru1_total_events if ru1_total_events > 0 else 0

    ru2_emissions = sum(c.emission_count for c in ru2_complexes)
    ru2_quenched = sum(c.quenched_count for c in ru2_complexes)
    ru2_total_events = ru2_emissions + ru2_quenched
    simulated_qy_ru2 = ru2_emissions / ru2_total_events if ru2_total_events > 0 else 0

    # Return results including parameters used
    result_data = params.copy() # Start with the input params
    result_data['Simulated_QY_Ru1'] = simulated_qy_ru1
    result_data['Simulated_QY_Ru2'] = simulated_qy_ru2
    result_data['Ru1_Events'] = ru1_total_events # Optional: track total events
    result_data['Ru2_Events'] = ru2_total_events # Optional: track total events

    return result_data


# --- Main Execution Block ---
if __name__ == "__main__":
    overall_start_time = time.time()
    all_results = []

    # Generate all combinations of parameters
    param_names = list(param_sweep_config.keys())
    param_values = list(param_sweep_config.values())
    param_combinations = list(itertools.product(*param_values))
    total_runs = len(param_combinations)

    print(f"--- Starting Parameter Sweep ---")
    print(f"Total simulation runs planned: {total_runs}")
    print(f"Results will be saved to: {RESULTS_FILENAME}")
    print(f"Parameters being varied: {param_names}")

    # Run simulations for each combination
    for i, combo in enumerate(param_combinations):
        run_params = dict(zip(param_names, combo))
        print(f"\nRunning simulation {i+1}/{total_runs} with parameters:")
        print(f"  {run_params}")
        run_start_time = time.time()

        # Execute the simulation
        result = run_simulation(run_params)

        run_end_time = time.time()
        print(f"  Run {i+1} finished in {run_end_time - run_start_time:.2f} seconds.")

        if result:
            all_results.append(result)
            print(f"  Results: QY_Ru1={result['Simulated_QY_Ru1']:.4f}, QY_Ru2={result['Simulated_QY_Ru2']:.4f}")
        else:
            print(f"  Run {i+1} failed or produced no results.")


    print(f"\n--- Parameter Sweep Finished ---")

    # Save results to CSV file
    if not all_results:
        print("No results were generated, skipping CSV file writing.")
    else:
        # Define CSV header based on the keys in the first result dictionary
        # Ensure consistent order by using the parameter names + calculated results
        fieldnames = param_names + ['Simulated_QY_Ru1', 'Simulated_QY_Ru2', 'Ru1_Events', 'Ru2_Events']
        # Make sure all keys exist in the results (handle potential missing optional keys)
        # fieldnames = list(all_results[0].keys()) # Alternative if all keys are guaranteed

        print(f"\nSaving {len(all_results)} results to {RESULTS_FILENAME}...")
        try:
            with open(RESULTS_FILENAME, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, extrasaction='ignore') # Ignore extra keys if any
                writer.writeheader()
                writer.writerows(all_results)
            print("Results saved successfully.")
        except IOError as e:
            print(f"Error writing results to CSV file: {e}")
        except Exception as e:
             print(f"An unexpected error occurred during CSV writing: {e}")


    overall_end_time = time.time()
    print(f"\nTotal execution time for all runs: {overall_end_time - overall_start_time:.2f} seconds")

