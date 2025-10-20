import numpy as np
import random

def calculate_cut(num_nodes, graph_edges, partition):
    """
    Calculates the size of the cut for a given partition (S, S_bar).

    Args:
        num_nodes (int): Total number of nodes (N=10).
        graph_edges (list of tuples): List of (i, j) connections.
        partition (list): A list where partition[i] is +1 (in S) or -1 (in S_bar).

    Returns:
        int: The size of the cut (number of edges crossing the partition).
    """
    cut_size = 0
    # The cut consists of edges where the endpoints are in different partitions
    # i.e., partition[i] * partition[j] == -1
    for i, j in graph_edges:
        # Note: We use i-1 and j-1 for 0-based indexing if your phases/graph
        # are 1-based, but generally it's safer to stick to 0-based from the start.
        # Assuming 0-based indexing for phases/partition:
        if partition[i] != partition[j]:
            cut_size += 1
            
    return cut_size

def randomized_rounding_maxcut(phases, graph_edges, num_trials=1000):
    """
    Applies the randomized rounding procedure to find the maximum cut.

    Args:
        phases (list or numpy.array): The stable phase angle (0 to 2*pi) for each node.
        graph_edges (list of tuples): List of (i, j) connections (0-indexed).
        num_trials (int): The number of random splitting angles to test.

    Returns:
        tuple: (max_cut_value, best_partition)
    """
    N = len(phases)
    best_cut_value = 0
    best_partition = None
    
    # Convert phases to a NumPy array for easier element-wise operations
    phases_array = np.array(phases)

    print(f"Starting randomized rounding for N={N} graph over {num_trials} trials.")

    for trial in range(num_trials):
        # 1. Choose a Random Splitting Angle (phi)
        phi = random.uniform(0, 2 * np.pi)

        # 2. Create the Discrete Partition
        
        # Calculate the centered phase: (theta_i - phi) mod 2pi
        centered_phases = (phases_array - phi) % (2 * np.pi)
        
        # Partition rule: 
        # If centered_phase is in [0, pi), assign +1 (Set S)
        # If centered_phase is in [pi, 2pi), assign -1 (Set S_bar)
        
        # Assign +1 if phase is in the [0, pi) half-circle
        partition = np.where(centered_phases < np.pi, 1, -1).tolist()
        
        # 3. Calculate the Cut Value
        current_cut_value = calculate_cut(N, graph_edges, partition)

        # 4. Update the Maximum
        if current_cut_value > best_cut_value:
            best_cut_value = current_cut_value
            best_partition = partition
            # Convert partition from [1, -1] to (S, S_bar) for clearer output
            S = [i for i, x in enumerate(best_partition) if x == 1]
            S_bar = [i for i, x in enumerate(best_partition) if x == -1]
            
            # print(f"  -> New Max Cut: {best_cut_value} at trial {trial+1}")


    # Convert the final best partition to the two sets S and S_bar
    final_S = [i for i, x in enumerate(best_partition) if x == 1]
    final_S_bar = [i for i, x in enumerate(best_partition) if x == -1]

    return best_cut_value, (final_S, final_S_bar)

# ----------------------------------------------------------------------
# Example Usage for a 10-Node Graph
# ----------------------------------------------------------------------

# NOTE: ALL NODES (0 to 9) MUST BE 0-INDEXED for the code to work!

# 1. Input: Graph Structure (Edges)
# This is an example of a small graph (a path graph with a cycle)
# You MUST replace this with the edges of your specific 10-node graph!
graph_edges_10_nodes = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5),
    (5, 6), (6, 7), (7, 8), (8, 9), (9, 0), # A cycle
    (0, 5), # A "long-range" edge
]

# 2. Input: Computed Phases
# These are EXAMPLE phases (in radians) you would get from your Kuramoto simulation.
# You MUST replace this with the actual phases you computed!
# Note: For the example graph above, the 'ideal' MaxCut would put half the nodes 
# near 0 and the other half near pi.
example_phases = [
    0.1,    # Node 0
    0.2,    # Node 1
    0.3,    # Node 2
    3.0,    # Node 3 (Close to pi)
    3.1,    # Node 4
    3.2,    # Node 5
    0.15,   # Node 6
    0.25,   # Node 7
    3.05,   # Node 8
    3.15    # Node 9
]

# 3. Run the Algorithm
max_cut_value, (set_S, set_S_bar) = randomized_rounding_maxcut(
    phases=example_phases, 
    graph_edges=graph_edges_10_nodes, 
    num_trials=2000 # Use more trials (e.g., 2000) for better results
)

# 4. Output Results
print("\n" + "="*40)
print("MAXCUT ROUNDING RESULTS")
print("="*40)
print(f"Maximum Cut Size Found: {max_cut_value}")
print(f"Partition S (+1): {set_S}")
print(f"Partition S_bar (-1): {set_S_bar}")
print(f"Total Edges in Graph: {len(graph_edges_10_nodes)}")
# The max possible cut for this example (11 edges) is 10.
