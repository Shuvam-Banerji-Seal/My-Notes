import numpy as np
import matplotlib.pyplot as plt

def generate_scc_lattice(n=3, a=1.0):
    """
    Generates atomic positions for a Simple Cubic (SCC) lattice.

    Args:
        n (int): Number of unit cells along each dimension.
        a (float): Lattice constant.

    Returns:
        np.ndarray: Array of shape (N, 3) with atomic coordinates.
    """
    atom_positions = []
    # SCC has only one atom at (0,0,0) per cell
    basis = [[0.0, 0.0, 0.0]]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                for b in basis:
                    atom_positions.append([
                        (i + b[0]) * a,
                        (j + b[1]) * a,
                        (k + b[2]) * a
                    ])
    return np.array(atom_positions)

def plot_scc_lattice(positions, n, a):
    """
    Plots the generated SCC lattice in 3D.
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], c='r', marker='o')

    ax.set_xlabel('X (Å)')
    ax.set_ylabel('Y (Å)')
    ax.set_zlabel('Z (Å)')
    ax.set_title(f'Simple Cubic Lattice: {n} × {n} × {n} Unit Cells')

    limit = n * a
    ax.set_xlim([0, limit])
    ax.set_ylim([0, limit])
    ax.set_zlim([0, limit])

    plt.show()

if __name__ == '__main__':
    n = 3     # Number of unit cells along each axis
    a = 1.0   # Lattice constant (Å)

    scc_positions = generate_scc_lattice(n, a)

    # Save to XYZ file
    with open('scc.xyz', 'w') as f:
        f.write(f"{len(scc_positions)}\n")
        f.write(f"SCC lattice: {n}x{n}x{n} unit cells, a={a} Å\n")
        for pos in scc_positions:
            f.write(f"C {pos[0]:.4f} {pos[1]:.4f} {pos[2]:.4f}\n")

    print(f"Generated {len(scc_positions)} atomic positions and saved to scc.xyz")

    plot_scc_lattice(scc_positions, n, a)
