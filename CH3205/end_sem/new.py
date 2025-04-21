import numpy as np
import random
import time
import math

# Optional: Import matplotlib for visualization if available
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.animation as animation
    VISUALIZE = True # Set to False if matplotlib is not installed or if you want faster execution
except ImportError:
    VISUALIZE = False
    print("Matplotlib not found. Visualization disabled.")
    print("Install it using: pip install matplotlib")

# --- Simulation Parameters ---
GRID_SIZE = 50        # Size of the simulation grid (GRID_SIZE x GRID_SIZE)
CORE_RADIUS = 15      # Characteristic radius defining the core region's density falloff
SURFACE_THICKNESS = 5 # How far from the core radius Ru(1) can be placed
NUM_RU1 = 30          # Number of Ru(1) complexes (surface)
NUM_RU2 = 30          # Number of Ru(2) complexes (core)
NUM_O2 = 180          # Number of Oxygen molecules
SIMULATION_STEPS = 600 # Number of time steps for the simulation
EXCITED_LIFETIME = 30 # Time steps an Ru complex stays excited if not quenched
QUENCHING_RADIUS = 1.8 # Distance within which O2 can quench Ru
QUENCHING_RADIUS_SQ = QUENCHING_RADIUS**2
# O2 Movement parameters (related to density)
O2_MOVE_PROB_MAX = 0.98 # Max probability (in low density regions)
O2_MOVE_PROB_MIN = 0.10 # Min probability (in high density regions)
DENSITY_STEEPNESS = 0.3 # Controls how quickly density falls off around CORE_RADIUS

# Visualization parameters
ANIMATION_INTERVAL = 50 # Milliseconds between animation frames
FRAMES_TO_SKIP = 1      # Update visualization every N frames (1 = update every frame)

# --- Classes ---
class RutheniumComplex:
    """ Represents a Ruthenium complex molecule. (Unchanged from previous version) """
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type # 'Ru1' (surface) or 'Ru2' (core)
        self.state = 'ground' # 'ground' or 'excited'
        self.excited_timer = 0
        self.emission_count = 0
        self.quenched_count = 0
        self.total_excitations = 0

    def excite(self):
        if self.state == 'ground':
            self.state = 'excited'
            self.excited_timer = EXCITED_LIFETIME
            self.total_excitations += 1

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

    def move(self, grid_size, core_center, core_radius):
        """ Moves the oxygen molecule randomly, hindered by polymer density. """
        # Calculate density based on distance from core center
        density = get_polymer_density(self.x, self.y, core_center, core_radius, DENSITY_STEEPNESS)

        # Calculate movement probability based on density
        # Probability decreases linearly from MAX to MIN as density goes from 0 to 1
        move_prob = O2_MOVE_PROB_MAX - density * (O2_MOVE_PROB_MAX - O2_MOVE_PROB_MIN)
        move_prob = max(O2_MOVE_PROB_MIN, min(O2_MOVE_PROB_MAX, move_prob)) # Clamp probability

        if random.random() < move_prob:
            # Move one step in a random direction (including staying put)
            dx = random.choice([-1, 0, 1])
            dy = random.choice([-1, 0, 1])

            # Apply boundary conditions (stay within grid)
            new_x = max(0, min(grid_size - 1, self.x + dx))
            new_y = max(0, min(grid_size - 1, self.y + dy))
            self.x = new_x
            self.y = new_y


# --- Helper Functions ---
def get_polymer_density(x, y, center, radius, steepness):
    """ Calculates a simulated polymer density based on distance from the center.
        Uses a sigmoid-like function for a smooth falloff.
        Density approaches 1 deep in the core and 0 far away.
    """
    dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
    # Sigmoid function centered around 'radius'
    density = 1 / (1 + math.exp(steepness * (dist - radius)))
    return density

def is_in_core_region(x, y, center, radius):
    """ Checks if coordinates (x, y) are within the nominal core radius (for placement). """
    # Use a simple radius check for initial placement purposes
    return (x - center[0])**2 + (y - center[1])**2 < radius**2

def place_complexes(num, type, grid_size, core_center, core_radius):
    """ Places Ru complexes either in the core region or near the surface region. """
    complexes = []
    attempts = 0
    max_attempts = num * 300 # Increase attempts for potentially trickier placement

    surface_outer_radius = core_radius + SURFACE_THICKNESS

    while len(complexes) < num and attempts < max_attempts:
        attempts += 1
        x = random.uniform(0, grid_size - 1)
        y = random.uniform(0, grid_size - 1)
        in_core_flag = is_in_core_region(x, y, core_center, core_radius)
        dist_from_center = math.sqrt((x - core_center[0])**2 + (y - core_center[1])**2)

        # Place Ru1 (Surface): Must be OUTSIDE core radius but WITHIN surface thickness boundary
        if type == 'Ru1' and not in_core_flag and dist_from_center < surface_outer_radius:
            complexes.append(RutheniumComplex(x, y, type))

        # Place Ru2 (Core): Must be INSIDE core radius
        elif type == 'Ru2' and in_core_flag:
            complexes.append(RutheniumComplex(x, y, type))

    if len(complexes) < num:
        print(f"Warning: Could only place {len(complexes)} of {num} desired {type} complexes. Try adjusting parameters.")
    return complexes

# --- Visualization Setup ---
fig, ax = None, None
ru1_scatter, ru2_scatter, o2_scatter = None, None, None
density_vis = None # For visualizing the density gradient

def setup_visualization(grid_size, core_center, core_radius):
    """ Sets up the matplotlib figure and axes for animation. """
    global fig, ax, ru1_scatter, ru2_scatter, o2_scatter, density_vis
    fig, ax = plt.subplots(figsize=(9, 9)) # Slightly larger figure

    # --- Create a visual representation of the density gradient ---
    n_grid = 100 # Resolution for density plot
    x_vis = np.linspace(0, grid_size-1, n_grid)
    y_vis = np.linspace(0, grid_size-1, n_grid)
    xx, yy = np.meshgrid(x_vis, y_vis)
    zz = np.zeros_like(xx)
    for i in range(n_grid):
        for j in range(n_grid):
            zz[i, j] = get_polymer_density(xx[i, j], yy[i, j], core_center, core_radius, DENSITY_STEEPNESS)

    # Display density as background image with transparency
    density_vis = ax.imshow(zz, extent=(0, grid_size-1, 0, grid_size-1), origin='lower',
                            cmap='Blues', alpha=0.4, vmin=0, vmax=1.2) # vmax slightly > 1 for visibility
    # Add a nominal core radius circle for reference
    core_patch = patches.Circle(core_center, core_radius, fill=False, color='grey', linestyle='--', alpha=0.7, label='Nominal Core Radius')
    ax.add_patch(core_patch)
    # --- End density visualization ---

    ax.set_xlim(0, grid_size)
    ax.set_ylim(0, grid_size)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title('Enhanced Ruthenium Polymer Simulation')

    # Placeholders for scatter plots
    # Use different markers and slightly larger size
    ru1_scatter = ax.scatter([], [], c='orangered', marker='o', s=40, edgecolor='black', linewidth=0.5, label='Ru(1) Surface')
    ru2_scatter = ax.scatter([], [], c='deepskyblue', marker='s', s=40, edgecolor='black', linewidth=0.5, label='Ru(2) Core')
    o2_scatter = ax.scatter([], [], c='dimgrey', marker='.', s=15, alpha=0.7, label='O2') # Smaller, grey O2

    ax.legend(loc='upper right', fontsize='small')
    plt.tight_layout()
    return fig, ax

# --- Animation Update Function ---
def update_frame(frame, ru1_complexes, ru2_complexes, o2_molecules, grid_size, core_center, core_radius, steps_per_frame):
    """ Updates the simulation state and plot for each animation frame. """
    global ru1_scatter, ru2_scatter, o2_scatter, ax

    # Run multiple simulation steps per frame for smoother animation feel
    for _ in range(steps_per_frame):
        # 1. Excite complexes (optional: could be probabilistic)
        for ru in ru1_complexes + ru2_complexes:
            ru.excite() # Simple continuous excitation

        # 2. Move Oxygen
        for o2 in o2_molecules:
            o2.move(grid_size, core_center, core_radius)

        # 3. Check for Quenching
        for ru in ru1_complexes + ru2_complexes:
            if ru.state == 'excited':
                for o2 in o2_molecules:
                    dist_sq = (ru.x - o2.x)**2 + (ru.y - o2.y)**2
                    if dist_sq < QUENCHING_RADIUS_SQ:
                        ru.quench()
                        break # Quenched

        # 4. Ru complexes evolve (timer/emission)
        for ru in ru1_complexes + ru2_complexes:
            ru.step()

    # --- Update Visualization Data ---
    # Ru(1) - orangered (excited) / darkred (ground)
    ru1_pos = np.array([[c.x, c.y] for c in ru1_complexes]) if ru1_complexes else np.empty((0, 2))
    ru1_colors = ['orangered' if c.state == 'excited' else 'darkred' for c in ru1_complexes]
    ru1_scatter.set_offsets(ru1_pos)
    ru1_scatter.set_facecolor(ru1_colors) # Update face color for state change

    # Ru(2) - deepskyblue (excited) / darkblue (ground)
    ru2_pos = np.array([[c.x, c.y] for c in ru2_complexes]) if ru2_complexes else np.empty((0, 2))
    ru2_colors = ['deepskyblue' if c.state == 'excited' else 'darkblue' for c in ru2_complexes]
    ru2_scatter.set_offsets(ru2_pos)
    ru2_scatter.set_facecolor(ru2_colors) # Update face color

    # Oxygen
    o2_pos = np.array([[o.x, o.y] for o in o2_molecules]) if o2_molecules else np.empty((0, 2))
    o2_scatter.set_offsets(o2_pos)

    ax.set_title(f'Enhanced Ruthenium Polymer Simulation - Step {frame * steps_per_frame}')

    # Return the updated scatter objects for blitting (optional, may not work reliably with facecolor changes)
    return ru1_scatter, ru2_scatter, o2_scatter,

# --- Main Simulation ---
if __name__ == "__main__":
    start_time = time.time()

    # --- Simulation Setup ---
    core_center = (GRID_SIZE / 2, GRID_SIZE / 2)

    print("Setting up enhanced simulation...")
    # Place Ru complexes
    ru1_complexes = place_complexes(NUM_RU1, 'Ru1', GRID_SIZE, core_center, CORE_RADIUS)
    ru2_complexes = place_complexes(NUM_RU2, 'Ru2', GRID_SIZE, core_center, CORE_RADIUS)
    print(f"Placed {len(ru1_complexes)} Ru(1) and {len(ru2_complexes)} Ru(2) complexes.")

    # Place O2 molecules (start them outside the core region)
    o2_molecules = []
    attempts = 0
    max_attempts = NUM_O2 * 100
    while len(o2_molecules) < NUM_O2 and attempts < max_attempts:
        attempts += 1
        x = random.uniform(0, GRID_SIZE - 1)
        y = random.uniform(0, GRID_SIZE - 1)
        # Ensure O2 starts in lower density region initially
        if get_polymer_density(x, y, core_center, CORE_RADIUS, DENSITY_STEEPNESS) < 0.3:
             o2_molecules.append(OxygenMolecule(x, y))
    if len(o2_molecules) < NUM_O2:
         print(f"Warning: Could only place {len(o2_molecules)} of {NUM_O2} O2 molecules initially.")
    print(f"Placed {len(o2_molecules)} O2 molecules.")

    # --- Run Simulation ---
    if VISUALIZE:
        print("Initializing visualization...")
        fig, ax = setup_visualization(GRID_SIZE, core_center, CORE_RADIUS)
        print("Starting animation...")
        # Calculate number of frames needed
        num_frames = SIMULATION_STEPS // FRAMES_TO_SKIP
        # Create animation
        ani = animation.FuncAnimation(fig, update_frame, frames=num_frames,
                                      fargs=(ru1_complexes, ru2_complexes, o2_molecules,
                                             GRID_SIZE, core_center, CORE_RADIUS, FRAMES_TO_SKIP),
                                      interval=ANIMATION_INTERVAL, blit=False, repeat=False) # blit=False often more reliable
        plt.show() # Display the animation window

        # After animation window is closed, run the simulation steps that might have been missed
        # Note: The animation runs the simulation. If the window is closed early,
        # the simulation stops. For full analysis, run non-visually or let animation finish.
        print("Animation finished or window closed.")
        # We will analyze the state *after* the animation ran.

    else:
        # Run simulation without visualization
        print(f"\n--- Running Simulation ({SIMULATION_STEPS} steps) without visualization ---")
        for step in range(SIMULATION_STEPS):
            # 1. Excite
            for ru in ru1_complexes + ru2_complexes: ru.excite()
            # 2. Move O2
            for o2 in o2_molecules: o2.move(GRID_SIZE, core_center, CORE_RADIUS)
            # 3. Quench
            for ru in ru1_complexes + ru2_complexes:
                if ru.state == 'excited':
                    for o2 in o2_molecules:
                        dist_sq = (ru.x - o2.x)**2 + (ru.y - o2.y)**2
                        if dist_sq < QUENCHING_RADIUS_SQ:
                            ru.quench()
                            break
            # 4. Evolve Ru
            for ru in ru1_complexes + ru2_complexes: ru.step()
            # Print progress
            if step % 100 == 0 or step == SIMULATION_STEPS - 1:
                 print(f"  Step {step+1}/{SIMULATION_STEPS} completed...")
        print("--- Simulation Finished ---")


    end_time = time.time()
    print(f"Total Execution Time: {end_time - start_time:.2f} seconds")

    # --- Results Analysis ---
    ru1_emissions = sum(c.emission_count for c in ru1_complexes)
    ru1_quenched = sum(c.quenched_count for c in ru1_complexes)
    ru1_total_events = ru1_emissions + ru1_quenched

    ru2_emissions = sum(c.emission_count for c in ru2_complexes)
    ru2_quenched = sum(c.quenched_count for c in ru2_complexes)
    ru2_total_events = ru2_emissions + ru2_quenched

    simulated_qy_ru1 = ru1_emissions / ru1_total_events if ru1_total_events > 0 else 0
    simulated_qy_ru2 = ru2_emissions / ru2_total_events if ru2_total_events > 0 else 0

    print("\n--- Simulation Results ---")
    print(f"Parameters:")
    print(f"  Grid: {GRID_SIZE}x{GRID_SIZE}, Core Radius: {CORE_RADIUS}, Density Steepness: {DENSITY_STEEPNESS}")
    print(f"  Num Ru(1): {len(ru1_complexes)}, Num Ru(2): {len(ru2_complexes)}, Num O2: {len(o2_molecules)}")
    print(f"  Lifetime: {EXCITED_LIFETIME} steps, Quench Radius: {QUENCHING_RADIUS}")
    print(f"  O2 Move Prob Range: [{O2_MOVE_PROB_MIN:.2f} - {O2_MOVE_PROB_MAX:.2f}]")
    print("-" * 25)
    print("Ru(1) - Surface Complexes:")
    print(f"  Total Decay Events: {ru1_total_events}")
    print(f"  Emissions Recorded: {ru1_emissions}")
    print(f"  Quenched Recorded:  {ru1_quenched}")
    print(f"  Simulated Quantum Yield: {simulated_qy_ru1:.4f}")
    print("-" * 25)
    print("Ru(2) - Core Complexes:")
    print(f"  Total Decay Events: {ru2_total_events}")
    print(f"  Emissions Recorded: {ru2_emissions}")
    print(f"  Quenched Recorded:  {ru2_quenched}")
    print(f"  Simulated Quantum Yield: {simulated_qy_ru2:.4f}")
    print("-" * 25)

    # --- Conclusion ---
    if ru1_total_events == 0 or ru2_total_events == 0:
        print("\nConclusion: No decay events recorded for one or both types.")
        print("Check parameters (e.g., SIMULATION_STEPS, EXCITED_LIFETIME) or placement.")
    elif simulated_qy_ru2 > simulated_qy_ru1:
        print("\nConclusion: As expected, the simulated QY for Core complexes (Ru2)")
        print(f"is higher ({simulated_qy_ru2:.4f}) than for Surface complexes (Ru1) ({simulated_qy_ru1:.4f}).")
        print("The density gradient model effectively simulates hindered O2 access to the core,")
        print("leading to less quenching and a higher probability of emission for Ru(2).")
    else:
        print("\nConclusion: Unexpected Result! Simulated QY for Surface (Ru1) is >= Core (Ru2).")
        print(f"  QY(Ru1) = {simulated_qy_ru1:.4f}, QY(Ru2) = {simulated_qy_ru2:.4f}")
        print("This might indicate insufficient density difference effect.")
        print("Consider adjusting DENSITY_STEEPNESS, O2_MOVE_PROB_MIN/MAX, CORE_RADIUS,")
        print("or increasing SIMULATION_STEPS or NUM_O2.")

