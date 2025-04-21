import numpy as np
import random
import time
import math
import argparse
from datetime import datetime
import json
import os

# Optional: Import matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import matplotlib.animation as animation
    from matplotlib.colors import LinearSegmentedColormap
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    VISUALIZE = True
except ImportError:
    VISUALIZE = False
    print("Matplotlib not found. Visualization disabled.")
    print("Install it using: pip install matplotlib")

# --- Command Line Arguments ---
def parse_arguments():
    parser = argparse.ArgumentParser(description='Enhanced Ruthenium Polymer Simulation')
    
    # Core simulation parameters
    parser.add_argument('--grid-size', type=int, default=50, help='Size of the simulation grid')
    parser.add_argument('--core-radius', type=float, default=15, help='Characteristic radius of the core region')
    parser.add_argument('--surface-thickness', type=float, default=5, help='Thickness of the surface layer')
    parser.add_argument('--num-ru1', type=int, default=30, help='Number of Ru(1) surface complexes')
    parser.add_argument('--num-ru2', type=int, default=30, help='Number of Ru(2) core complexes')
    parser.add_argument('--num-o2', type=int, default=180, help='Number of oxygen molecules')
    parser.add_argument('--steps', type=int, default=600, help='Number of simulation time steps')
    
    # Physical model parameters
    parser.add_argument('--excited-lifetime', type=int, default=30, help='Excited state lifetime in time steps')
    parser.add_argument('--quenching-radius', type=float, default=1.8, help='Distance for quenching')
    parser.add_argument('--o2-prob-max', type=float, default=0.98, help='Maximum O2 movement probability')
    parser.add_argument('--o2-prob-min', type=float, default=0.10, help='Minimum O2 movement probability')
    parser.add_argument('--density-steepness', type=float, default=0.3, help='Steepness of density gradient')
    parser.add_argument('--excitation-prob', type=float, default=1.0, help='Probability of excitation per time step')
    
    # Visualization/run options
    parser.add_argument('--visualize', action='store_true', help='Enable visualization')
    parser.add_argument('--no-vis', action='store_false', dest='visualize', help='Disable visualization')
    parser.add_argument('--animation-interval', type=int, default=50, help='Animation interval in milliseconds')
    parser.add_argument('--frames-to-skip', type=int, default=1, help='Frames to skip in animation')
    parser.add_argument('--save-animation', action='store_true', help='Save animation to file')
    parser.add_argument('--save-path', type=str, default='simulation_results', help='Path to save results')
    parser.add_argument('--save-data', action='store_true', help='Save simulation data to file')
    parser.add_argument('--high-res', action='store_true', help='Use high resolution for visualization')
    
    parser.set_defaults(visualize=True)
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
        self.position_history = []  # Optional: track positions over time
        
    def excite(self, excitation_prob=1.0, lifetime=30):
        """Excite the complex with given probability and lifetime"""
        if self.state == 'ground' and random.random() < excitation_prob:
            self.state = 'excited'
            self.excited_timer = lifetime
            self.total_excitations += 1
            # Record initial position when excited
            self.position_history.append((self.x, self.y))

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
    
    def get_average_lifetime(self):
        """Calculate average excited state lifetime across all events"""
        return sum(self.lifetime_history) / len(self.lifetime_history) if self.lifetime_history else 0
    
    def get_lifetime_distribution(self):
        """Return histogram data for lifetime distribution"""
        return self.lifetime_history
    
    def to_dict(self):
        """Convert complex data to dictionary for serialization"""
        return {
            'type': self.type,
            'position': (self.x, self.y),
            'emissions': self.emission_count,
            'quenched': self.quenched_count,
            'total_excitations': self.total_excitations,
            'avg_lifetime': self.get_average_lifetime(),
            'quantum_yield': self.get_simulated_qy()
        }

class OxygenMolecule:
    """ Represents an Oxygen molecule (quencher) with enhanced tracking. """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.quench_count = 0
        self.path_length = 0
        self.position_history = []  # Optional: track positions over time
        
    def move(self, grid_size, core_center, core_radius, density_steepness, prob_min, prob_max):
        """ Moves the oxygen molecule with density-dependent probability. """
        # Store previous position
        prev_x, prev_y = self.x, self.y
        
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
            
            # Calculate distance moved
            dist_moved = math.sqrt((new_x - prev_x)**2 + (new_y - prev_y)**2)
            self.path_length += dist_moved
            
            # Optionally record position
            self.position_history.append((self.x, self.y))
    
    def record_quench(self):
        """Record a quenching event by this O2 molecule"""
        self.quench_count += 1
    
    def get_average_velocity(self, time_steps):
        """Calculate average velocity over simulation"""
        return self.path_length / time_steps if time_steps > 0 else 0
    
    def to_dict(self):
        """Convert O2 data to dictionary for serialization"""
        return {
            'position': (self.x, self.y),
            'quench_count': self.quench_count,
            'path_length': self.path_length
        }

# --- Helper Functions ---
def get_polymer_density(x, y, center, radius, steepness):
    """ Calculates polymer density using a sigmoid-like function. """
    dist = math.sqrt((x - center[0])**2 + (y - center[1])**2)
    # Sigmoid function centered around 'radius'
    # Using a safe approach to prevent potential overflow
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

def calculate_o2_distribution(o2_molecules, grid_size, n_bins=10):
    """Calculate the spatial distribution of O2 molecules"""
    bin_edges = np.linspace(0, grid_size, n_bins+1)
    o2_positions = np.array([(o2.x, o2.y) for o2 in o2_molecules])
    
    # Create 2D histogram
    if len(o2_positions) > 0:
        H, xedges, yedges = np.histogram2d(
            o2_positions[:, 0], o2_positions[:, 1], 
            bins=[bin_edges, bin_edges]
        )
        return H, xedges, yedges
    else:
        # Return empty histogram if no O2 molecules
        return np.zeros((n_bins, n_bins)), bin_edges, bin_edges

# --- Visualization Functions ---
def setup_visualization(grid_size, core_center, core_radius, surface_thickness, density_steepness, high_res=False):
    """ Sets up the matplotlib figure with enhanced visualization. """
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(16, 10))
    fig.suptitle('Enhanced Ruthenium Polymer Simulation', fontsize=16)
    
    # Main simulation area
    ax_main = plt.subplot2grid((2, 3), (0, 0), colspan=2, rowspan=2)
    
    # Side panels for statistics
    ax_stats_ru1 = plt.subplot2grid((2, 3), (0, 2))
    ax_stats_ru2 = plt.subplot2grid((2, 3), (1, 2))
    
    # Resolution for density plot
    n_grid = 200 if high_res else 100  
    x_vis = np.linspace(0, grid_size-1, n_grid)
    y_vis = np.linspace(0, grid_size-1, n_grid)
    xx, yy = np.meshgrid(x_vis, y_vis)
    zz = np.zeros_like(xx)
    
    # Calculate density
    for i in range(n_grid):
        for j in range(n_grid):
            zz[i, j] = get_polymer_density(xx[i, j], yy[i, j], core_center, core_radius, density_steepness)
    
    # Create a custom colormap with better color scaling
    colors = [(0.95, 0.95, 1.0), (0.8, 0.8, 0.95), (0.6, 0.6, 0.9), (0.4, 0.4, 0.8)]
    custom_cmap = LinearSegmentedColormap.from_list('custom_blues', colors, N=256)
    
    # Display density as background image with transparency
    density_vis = ax_main.imshow(zz, extent=(0, grid_size-1, 0, grid_size-1), origin='lower',
                            cmap=custom_cmap, alpha=0.4, vmin=0, vmax=1.2)
    
    # Add colorbar for density
    divider = make_axes_locatable(ax_main)
    cax = divider.append_axes("right", size="3%", pad=0.05)
    cbar = plt.colorbar(density_vis, cax=cax)
    cbar.set_label('Polymer Density')
    
    # Add circles for core and surface regions
    core_patch = patches.Circle(core_center, core_radius, fill=False, color='grey', 
                              linestyle='--', alpha=0.7, label='Core Boundary')
    surface_patch = patches.Circle(core_center, core_radius + surface_thickness, fill=False, 
                                 color='darkgrey', linestyle=':', alpha=0.7, label='Surface Boundary')
    ax_main.add_patch(core_patch)
    ax_main.add_patch(surface_patch)
    
    # Configure main plot
    ax_main.set_xlim(0, grid_size)
    ax_main.set_ylim(0, grid_size)
    ax_main.set_aspect('equal', adjustable='box')
    ax_main.set_xlabel('X position')
    ax_main.set_ylabel('Y position')
    ax_main.set_title('Simulation Space')
    
    # Placeholders for scatter plots
    ru1_scatter = ax_main.scatter([], [], c='orangered', marker='o', s=40, 
                               edgecolor='black', linewidth=0.5, label='Ru(1) Surface')
    ru2_scatter = ax_main.scatter([], [], c='deepskyblue', marker='s', s=40, 
                               edgecolor='black', linewidth=0.5, label='Ru(2) Core')
    o2_scatter = ax_main.scatter([], [], c='dimgrey', marker='.', s=15, 
                              alpha=0.7, label='O2')
    
    # Set up stats axes
    ax_stats_ru1.set_title('Ru1 (Surface) Statistics')
    ax_stats_ru1.axis('off')  # Will use text instead of plots initially
    
    ax_stats_ru2.set_title('Ru2 (Core) Statistics')
    ax_stats_ru2.axis('off')  # Will use text instead of plots initially
    
    # Add legend to main plot
    ax_main.legend(loc='upper right', fontsize='small')
    
    # Add placeholder for stats text
    ru1_text = ax_stats_ru1.text(0.05, 0.95, 'Initializing...', transform=ax_stats_ru1.transAxes,
                               verticalalignment='top', wrap=True)
    ru2_text = ax_stats_ru2.text(0.05, 0.95, 'Initializing...', transform=ax_stats_ru2.transAxes,
                               verticalalignment='top', wrap=True)
    
    plt.tight_layout()
    return fig, (ax_main, ax_stats_ru1, ax_stats_ru2), (ru1_scatter, ru2_scatter, o2_scatter), (ru1_text, ru2_text)

def update_frame(frame, ru1_complexes, ru2_complexes, o2_molecules, args, sim_data):
    """ Updates visualization for one animation frame with enhanced statistics """
    # Unpack objects
    axes, scatters, texts = sim_data['axes'], sim_data['scatters'], sim_data['texts']
    ax_main, ax_stats_ru1, ax_stats_ru2 = axes
    ru1_scatter, ru2_scatter, o2_scatter = scatters
    ru1_text, ru2_text = texts
    
    # Unpack parameters
    grid_size = args.grid_size
    core_center = (grid_size / 2, grid_size / 2)
    core_radius = args.core_radius
    density_steepness = args.density_steepness
    steps_per_frame = args.frames_to_skip
    excited_lifetime = args.excited_lifetime
    quenching_radius_sq = args.quenching_radius ** 2
    o2_prob_min = args.o2_prob_min
    o2_prob_max = args.o2_prob_max
    excitation_prob = args.excitation_prob
    
    # Track frame time for analysis of simulation speed
    frame_start_time = time.time()
    
    # Run multiple simulation steps per frame
    for _ in range(steps_per_frame):
        # 1. Excite complexes with probability
        for ru in ru1_complexes + ru2_complexes:
            ru.excite(excitation_prob, excited_lifetime)

        # 2. Move Oxygen
        for o2 in o2_molecules:
            o2.move(grid_size, core_center, core_radius, density_steepness, o2_prob_min, o2_prob_max)

        # 3. Check for Quenching
        for ru in ru1_complexes + ru2_complexes:
            if ru.state == 'excited':
                for o2 in o2_molecules:
                    dist_sq = (ru.x - o2.x)**2 + (ru.y - o2.y)**2
                    if dist_sq < quenching_radius_sq:
                        ru.quench(math.sqrt(dist_sq))  # Pass actual distance
                        o2.record_quench()  # Record quench event for this O2
                        break  # Quenched

        # 4. Ru complexes evolve (timer/emission)
        for ru in ru1_complexes + ru2_complexes:
            ru.step()
    
    # Update core visualization data
    # Ru(1) complexes
    ru1_pos = np.array([[c.x, c.y] for c in ru1_complexes]) if ru1_complexes else np.empty((0, 2))
    ru1_colors = ['orangered' if c.state == 'excited' else 'darkred' for c in ru1_complexes]
    ru1_scatter.set_offsets(ru1_pos)
    ru1_scatter.set_facecolor(ru1_colors)
    
    # Ru(2) complexes
    ru2_pos = np.array([[c.x, c.y] for c in ru2_complexes]) if ru2_complexes else np.empty((0, 2))
    ru2_colors = ['deepskyblue' if c.state == 'excited' else 'darkblue' for c in ru2_complexes]
    ru2_scatter.set_offsets(ru2_pos)
    ru2_scatter.set_facecolor(ru2_colors)
    
    # Oxygen molecules
    o2_pos = np.array([[o.x, o.y] for o in o2_molecules]) if o2_molecules else np.empty((0, 2))
    o2_scatter.set_offsets(o2_pos)
    
    # Calculate current statistics for text displays
    current_step = frame * steps_per_frame
    sim_percent = (current_step / args.steps) * 100
    
    # Calculate quantum yields
    ru1_emissions = sum(c.emission_count for c in ru1_complexes)
    ru1_quenched = sum(c.quenched_count for c in ru1_complexes)
    ru1_total_events = ru1_emissions + ru1_quenched
    simulated_qy_ru1 = ru1_emissions / ru1_total_events if ru1_total_events > 0 else 0
    
    ru2_emissions = sum(c.emission_count for c in ru2_complexes)
    ru2_quenched = sum(c.quenched_count for c in ru2_complexes)
    ru2_total_events = ru2_emissions + ru2_quenched
    simulated_qy_ru2 = ru2_emissions / ru2_total_events if ru2_total_events > 0 else 0
    
    # Count currently excited complexes
    ru1_excited = sum(1 for c in ru1_complexes if c.state == 'excited')
    ru2_excited = sum(1 for c in ru2_complexes if c.state == 'excited')
    
    # Update statistics displays
    ru1_stats = (
        f"Step: {current_step}/{args.steps} ({sim_percent:.1f}%)\n"
        f"Emissions: {ru1_emissions}\n"
        f"Quenched: {ru1_quenched}\n"
        f"Currently Excited: {ru1_excited}/{len(ru1_complexes)}\n"
        f"Quantum Yield: {simulated_qy_ru1:.4f}\n"
    )
    
    ru2_stats = (
        f"Step: {current_step}/{args.steps} ({sim_percent:.1f}%)\n"
        f"Emissions: {ru2_emissions}\n"
        f"Quenched: {ru2_quenched}\n"
        f"Currently Excited: {ru2_excited}/{len(ru2_complexes)}\n"
        f"Quantum Yield: {simulated_qy_ru2:.4f}\n"
    )
    
    # Update texts
    ru1_text.set_text(ru1_stats)
    ru2_text.set_text(ru2_stats)
    
    # Update main title with progress
    ax_main.set_title(f'Simulation Progress: {sim_percent:.1f}% (Step {current_step}/{args.steps})')
    
    # Calculate frame time and update predicted completion
    frame_time = time.time() - frame_start_time
    frames_remaining = (args.steps // steps_per_frame) - frame - 1
    estimated_time = frames_remaining * frame_time
    
    # Record performance data
    sim_data['frame_times'].append(frame_time)
    
    # If this is the last frame, prepare for final analysis
    if current_step >= args.steps - steps_per_frame:
        sim_data['final_stats'] = {
            'ru1_qy': simulated_qy_ru1,
            'ru2_qy': simulated_qy_ru2,
            'ru1_emissions': ru1_emissions,
            'ru1_quenched': ru1_quenched,
            'ru2_emissions': ru2_emissions,
            'ru2_quenched': ru2_quenched
        }
    
    return ru1_scatter, ru2_scatter, o2_scatter, ru1_text, ru2_text

def generate_final_analysis(ru1_complexes, ru2_complexes, o2_molecules, args, start_time):
    """Generate comprehensive final analysis visualizations and data"""
    # Create a new figure for final analysis
    fig_final = plt.figure(figsize=(15, 12))
    fig_final.suptitle('Final Analysis: Ruthenium Complex Simulation', fontsize=16)
    
    # Calculate overall statistics
    ru1_emissions = sum(c.emission_count for c in ru1_complexes)
    ru1_quenched = sum(c.quenched_count for c in ru1_complexes)
    ru1_total_events = ru1_emissions + ru1_quenched
    simulated_qy_ru1 = ru1_emissions / ru1_total_events if ru1_total_events > 0 else 0
    
    ru2_emissions = sum(c.emission_count for c in ru2_complexes)
    ru2_quenched = sum(c.quenched_count for c in ru2_complexes)
    ru2_total_events = ru2_emissions + ru2_quenched
    simulated_qy_ru2 = ru2_emissions / ru2_total_events if ru2_total_events > 0 else 0
    
    # 1. Bar plot comparing emissions vs quenching
    ax1 = plt.subplot2grid((3, 3), (0, 0))
    labels = ['Ru1 (Surface)', 'Ru2 (Core)']
    emissions = [ru1_emissions, ru2_emissions]
    quenched = [ru1_quenched, ru2_quenched]
    
    x = np.arange(len(labels))
    width = 0.35
    
    ax1.bar(x - width/2, emissions, width, label='Emissions', color='green', alpha=0.7)
    ax1.bar(x + width/2, quenched, width, label='Quenched', color='red', alpha=0.7)
    
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels)
    ax1.set_ylabel('Count')
    ax1.set_title('Emissions vs Quenching')
    ax1.legend()
    
    # 2. QY comparison
    ax2 = plt.subplot2grid((3, 3), (0, 1))
    ax2.bar(labels, [simulated_qy_ru1, simulated_qy_ru2], color=['orangered', 'deepskyblue'])
    ax2.set_ylim(0, 1)
    ax2.set_ylabel('Quantum Yield')
    ax2.set_title('Quantum Yield Comparison')
    
    for i, v in enumerate([simulated_qy_ru1, simulated_qy_ru2]):
        ax2.text(i, v + 0.02, f'{v:.4f}', ha='center')
    
    # 3. Lifetime distributions
    ax3 = plt.subplot2grid((3, 3), (0, 2))
    ru1_lifetimes = [lt for c in ru1_complexes for lt in c.lifetime_history]
    ru2_lifetimes = [lt for c in ru2_complexes for lt in c.lifetime_history]
    
    if ru1_lifetimes and ru2_lifetimes:
        max_lifetime = max(max(ru1_lifetimes) if ru1_lifetimes else 0, 
                         max(ru2_lifetimes) if ru2_lifetimes else 0)
        bins = np.linspace(0, max_lifetime, 20)
        
        ax3.hist(ru1_lifetimes, bins=bins, alpha=0.5, label='Ru1', color='orangered')
        ax3.hist(ru2_lifetimes, bins=bins, alpha=0.5, label='Ru2', color='deepskyblue')
        ax3.set_xlabel('Excited State Duration')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Lifetime Distributions')
        ax3.legend()
    
    # 4. O2 distribution heatmap
    ax4 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
    H, xedges, yedges = calculate_o2_distribution(o2_molecules, args.grid_size, n_bins=20)
    im = ax4.imshow(H.T, origin='lower', extent=[0, args.grid_size, 0, args.grid_size], 
                  cmap='Reds', interpolation='nearest')
    
    # Add core and surface boundaries
    core_center = (args.grid_size / 2, args.grid_size / 2)
    core_patch = patches.Circle(core_center, args.core_radius, fill=False, color='black', 
                              linestyle='--', label='Core Boundary')
    surface_patch = patches.Circle(core_center, args.core_radius + args.surface_thickness, 
                                 fill=False, color='black', linestyle=':', label='Surface Boundary')
    ax4.add_patch(core_patch)
    ax4.add_patch(surface_patch)
    
    cbar = plt.colorbar(im, ax=ax4)
    cbar.set_label('O2 Concentration')
    ax4.set_title('Final O2 Distribution')
    ax4.set_xlabel('X position')
    ax4.set_ylabel('Y position')
    
    # 5. Simulation summary text
    ax5 = plt.subplot2grid((3, 3), (1, 2))
    ax5.axis('off')
    
    total_time = time.time() - start_time
    
# Complete the summary_text section
    summary_text = (
        f"Simulation Summary\n"
        f"------------------\n"
        f"Grid Size: {args.grid_size}x{args.grid_size}\n"
        f"Core Radius: {args.core_radius}\n"
        f"Surface Thickness: {args.surface_thickness}\n"
        f"Ru1 (Surface): {len(ru1_complexes)}\n"
        f"Ru2 (Core): {len(ru2_complexes)}\n"
        f"O2 Molecules: {len(o2_molecules)}\n"
        f"Steps: {args.steps}\n"
        f"Excited Lifetime: {args.excited_lifetime}\n"
        f"Quenching Radius: {args.quenching_radius}\n"
        f"Ru1 QY: {simulated_qy_ru1:.4f}\n"
        f"Ru2 QY: {simulated_qy_ru2:.4f}\n"
        f"Total Runtime: {total_time:.2f} seconds"
    )
    
    ax5.text(0.05, 0.95, summary_text, transform=ax5.transAxes,
            verticalalignment='top', fontfamily='monospace')
    
    # 6. O2 quenching activity
    ax6 = plt.subplot2grid((3, 3), (2, 0))
    o2_quench_counts = [o2.quench_count for o2 in o2_molecules]
    if o2_quench_counts:
        max_quenches = max(o2_quench_counts)
        bins = np.arange(0, max_quenches + 2) - 0.5
        ax6.hist(o2_quench_counts, bins=bins, color='purple', alpha=0.7)
        ax6.set_xlabel('Quenches per O2 Molecule')
        ax6.set_ylabel('Frequency')
        ax6.set_title('O2 Quenching Activity')
    
    # 7. Position plot with events
    ax7 = plt.subplot2grid((3, 3), (2, 1), colspan=2)
    
    # Plot polymer density background
    n_grid = 100
    x_vis = np.linspace(0, args.grid_size-1, n_grid)
    y_vis = np.linspace(0, args.grid_size-1, n_grid)
    xx, yy = np.meshgrid(x_vis, y_vis)
    zz = np.zeros_like(xx)
    
    # Calculate density
    core_center = (args.grid_size / 2, args.grid_size / 2)
    for i in range(n_grid):
        for j in range(n_grid):
            zz[i, j] = get_polymer_density(xx[i, j], yy[i, j], core_center, args.core_radius, args.density_steepness)
    
    # Create a custom colormap
    colors = [(0.95, 0.95, 1.0), (0.8, 0.8, 0.95), (0.6, 0.6, 0.9), (0.4, 0.4, 0.8)]
    custom_cmap = LinearSegmentedColormap.from_list('custom_blues', colors, N=256)
    
    # Display density as background
    ax7.imshow(zz, extent=(0, args.grid_size-1, 0, args.grid_size-1), origin='lower',
              cmap=custom_cmap, alpha=0.4, vmin=0, vmax=1)
    
    # Plot complexes colored by activity
    for c in ru1_complexes:
        total = c.emission_count + c.quenched_count
        if total > 0:
            size = 20 + 80 * (total / max(1, max(ru1_total_events/len(ru1_complexes), 
                                                ru2_total_events/len(ru2_complexes))))
            ax7.scatter(c.x, c.y, s=size, c='orangered', alpha=0.7, edgecolor='black')
    
    for c in ru2_complexes:
        total = c.emission_count + c.quenched_count
        if total > 0:
            size = 20 + 80 * (total / max(1, max(ru1_total_events/len(ru1_complexes), 
                                                ru2_total_events/len(ru2_complexes))))
            ax7.scatter(c.x, c.y, s=size, c='deepskyblue', alpha=0.7, edgecolor='black')
    
    # Add core and surface boundaries
    core_patch = patches.Circle(core_center, args.core_radius, fill=False, color='black', 
                              linestyle='--', label='Core Boundary')
    surface_patch = patches.Circle(core_center, args.core_radius + args.surface_thickness, 
                                 fill=False, color='black', linestyle=':', label='Surface Boundary')
    ax7.add_patch(core_patch)
    ax7.add_patch(surface_patch)
    
    ax7.set_xlabel('X position')
    ax7.set_ylabel('Y position')
    ax7.set_title('Complex Activity Map (size = activity)')
    
    plt.tight_layout()
    return fig_final

def save_simulation_data(ru1_complexes, ru2_complexes, o2_molecules, args, start_time, save_path):
    """Save simulation data to JSON file"""
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Prepare data dictionary
    data = {
        "parameters": vars(args),
        "runtime": time.time() - start_time,
        "timestamp": datetime.now().isoformat(),
        "results": {
            "ru1_complexes": [c.to_dict() for c in ru1_complexes],
            "ru2_complexes": [c.to_dict() for c in ru2_complexes],
            "o2_molecules": [o2.to_dict() for o in o2_molecules],
            "summary": {
                "ru1_count": len(ru1_complexes),
                "ru2_count": len(ru2_complexes),
                "o2_count": len(o2_molecules),
                "ru1_emissions": sum(c.emission_count for c in ru1_complexes),
                "ru1_quenched": sum(c.quenched_count for c in ru1_complexes),
                "ru2_emissions": sum(c.emission_count for c in ru2_complexes),
                "ru2_quenched": sum(c.quenched_count for c in ru2_complexes),
                "ru1_quantum_yield": sum(c.emission_count for c in ru1_complexes) / 
                                    max(1, sum(c.emission_count + c.quenched_count for c in ru1_complexes)),
                "ru2_quantum_yield": sum(c.emission_count for c in ru2_complexes) / 
                                    max(1, sum(c.emission_count + c.quenched_count for c in ru2_complexes))
            }
        }
    }
    
    # Save to file
    filename = os.path.join(save_path, f"simulation_data_{timestamp}.json")
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Simulation data saved to: {filename}")
    return filename

# --- Main Simulation Function ---
def run_simulation(args):
    """Run the complete simulation with all enhancements"""
    # Record start time
    start_time = time.time()
    
    # Set up grid and calculate centers
    grid_size = args.grid_size
    core_center = (grid_size / 2, grid_size / 2)
    
    # Initialize simulation elements
    print("Initializing simulation components...")
    
    # Place Ru complexes
    ru1_complexes = place_complexes(args.num_ru1, 'Ru1', grid_size, core_center, 
                                   args.core_radius, args.surface_thickness)
    ru2_complexes = place_complexes(args.num_ru2, 'Ru2', grid_size, core_center, 
                                   args.core_radius, args.surface_thickness)
    
    # Place O2 molecules with distribution weighted by polymer density
    o2_molecules = []
    attempts = 0
    max_attempts = args.num_o2 * 10
    
    while len(o2_molecules) < args.num_o2 and attempts < max_attempts:
        attempts += 1
        x = random.uniform(0, grid_size - 1)
        y = random.uniform(0, grid_size - 1)
        
        # Calculate probability based on density
        density = get_polymer_density(x, y, core_center, args.core_radius, args.density_steepness)
        if random.random() < density:
            o2_molecules.append(OxygenMolecule(x, y))
    
    print(f"Placed {len(ru1_complexes)} Ru1, {len(ru2_complexes)} Ru2, and {len(o2_molecules)} O2 molecules.")
    
    # Set up visualization if enabled
    if args.visualize and VISUALIZE:
        fig, axes, scatters, texts = setup_visualization(
            grid_size, core_center, args.core_radius, args.surface_thickness, 
            args.density_steepness, args.high_res
        )
        
        # Data storage for animation
        sim_data = {
            'axes': axes,
            'scatters': scatters,
            'texts': texts,
            'frame_times': [],
            'final_stats': {}
        }
        
        # Create animation
        frames = args.steps // args.frames_to_skip
        ani = animation.FuncAnimation(
            fig, update_frame, frames=frames,
            fargs=(ru1_complexes, ru2_complexes, o2_molecules, args, sim_data),
            interval=args.animation_interval, blit=True
        )
        
        # Save animation if requested
        if args.save_animation:
            print("Saving animation... (this may take a while)")
            os.makedirs(args.save_path, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            ani.save(f"{args.save_path}/simulation_{timestamp}.mp4", writer='ffmpeg', dpi=150)
        
        # Show animation
        plt.show()
        
        # Generate and display final analysis
        final_fig = generate_final_analysis(ru1_complexes, ru2_complexes, o2_molecules, args, start_time)
        
        # Save final analysis figure if requested
        if args.save_animation:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            final_fig.savefig(f"{args.save_path}/final_analysis_{timestamp}.png", dpi=150)
        
        plt.show()
    else:
        # Run simulation without visualization
        print("Running simulation without visualization...")
        for step in range(args.steps):
            # Print progress
            if step % (args.steps // 10) == 0:
                print(f"Progress: {step / args.steps * 100:.1f}%")
            
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
    
    # Save simulation data if requested
    if args.save_data:
        save_simulation_data(ru1_complexes, ru2_complexes, o2_molecules, args, start_time, args.save_path)
    
    # Print final results
    ru1_emissions = sum(c.emission_count for c in ru1_complexes)
    ru1_quenched = sum(c.quenched_count for c in ru1_complexes)
    ru1_total_events = ru1_emissions + ru1_quenched
    simulated_qy_ru1 = ru1_emissions / ru1_total_events if ru1_total_events > 0 else 0
    
    ru2_emissions = sum(c.emission_count for c in ru2_complexes)
    ru2_quenched = sum(c.quenched_count for c in ru2_complexes)
    ru2_total_events = ru2_emissions + ru2_quenched
    simulated_qy_ru2 = ru2_emissions / ru2_total_events if ru2_total_events > 0 else 0
    
    print("\nSimulation Complete!")
    print(f"Runtime: {time.time() - start_time:.2f} seconds")
    print(f"Ru1 (Surface) - QY: {simulated_qy_ru1:.4f} ({ru1_emissions} emissions / {ru1_total_events} events)")
    print(f"Ru2 (Core) - QY: {simulated_qy_ru2:.4f} ({ru2_emissions} emissions / {ru2_total_events} events)")
    
    return ru1_complexes, ru2_complexes, o2_molecules

# --- Main Entry Point ---
if __name__ == "__main__":
    args = parse_arguments()
    print("Ruthenium Polymer Simulation")
    print("=" * 30)
    print(f"Grid Size: {args.grid_size}x{args.grid_size}")
    print(f"Core Radius: {args.core_radius}, Surface Thickness: {args.surface_thickness}")
    print(f"Ru1: {args.num_ru1}, Ru2: {args.num_ru2}, O2: {args.num_o2}")
    print(f"Steps: {args.steps}")
    
    # Create save directory if needed
    if args.save_animation or args.save_data:
        os.makedirs(args.save_path, exist_ok=True)
    
    # Run the simulation
    ru1, ru2, o2 = run_simulation(args)