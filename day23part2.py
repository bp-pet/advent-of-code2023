import numpy as np
import networkx as nx

with open("day23.txt", "r") as f:
    raw = f.read()

grid = np.array([list(i) for i in raw.split("\n")])
slopes = [">", "<", "v", "^"]

def grid_to_string():
    result = ""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            result += grid[i, j]
        result += "\n"
    return result

def get_neighbors(pos):
    """Get all non # tiles around a given tile"""
    neighbors = []
    for i in [-1, 1]:
        # for vertical neighbors have to check if we are at boundary
        if pos[0] == 0 and i == -1:
            continue
        if pos[0] == grid.shape[0] - 1 and i == 1:
            continue
        if grid[pos[0] + i, pos[1]] != "#":
            neighbors.append((pos[0] + i, pos[1]))
    for j in [-1, 1]:
        if grid[pos[0], pos[1] + j] != "#":
            neighbors.append((pos[0], pos[1] + j))
    return neighbors

def get_nodes():
    """Record the nodes, which are the tiles with more than 2 neighbors"""
    nodes = [(0, 1), (grid.shape[0] - 1, grid.shape[1] - 2)]
    for i in range(1, grid.shape[0] - 1):
        for j in range(grid.shape[1]):
            if grid[i, j] != "#":
                if len(get_neighbors((i, j))) > 2:
                    nodes.append((i, j))
    return nodes

nodes = get_nodes()

# dict to map each node to its index for the adjacency matrix
nodes_dict = {nodes[i]: i for i in range(len(nodes))}

def check_for_neighboring_nodes():
    for i, node1 in enumerate(nodes):
        for node2 in nodes[i+1:]:
            if abs(node1[0] - node2[0]) + abs(node1[1] - node2[1]) < 2:
                raise Exception("Neighboring nodes detected")

check_for_neighboring_nodes()

adj = np.zeros([len(nodes), len(nodes)])

def add_edge(node1, node2, weight, slope_type):
    """Add an edge to the adjacency matrix"""
    slope_type = None
    if slope_type is None:
        adj[nodes_dict[node1], nodes_dict[node2]] = weight
        adj[nodes_dict[node2], nodes_dict[node1]] = weight
    if slope_type == -1:
        node1, node2 = node2, node1
    adj[nodes_dict[node1], nodes_dict[node2]] = weight

def get_direction(start_tile, end_tile):
    return (end_tile[0] - start_tile[0], end_tile[1] - start_tile[1])

def determine_slope_type(slope, direction):
    """Slope type is 1 if slope points towards the given direction
    of movement, -1 otherwise."""
    if slope == ">" and direction == (0, 1):
        return -1
    elif slope == ">" and direction == (0, -1):
        return 1
    elif slope == "<" and direction == (0, 1):
        return 1
    elif slope == "<" and direction == (0, -1):
        return -1
    elif slope == "v" and direction == (1, 0):
        return -1
    elif slope == "v" and direction == (-1, 0):
        return 1
    elif slope == "^" and direction == (1, 0):
        return 1
    elif slope == "^" and direction == (-1, 0):
        return -1
    else:
        raise Exception("Something wrong with slope")

def grid_to_graph():
    """Create a graph where the nodes are the junctions in the grid."""
    visited = np.zeros_like(grid, dtype=bool)
    for node in nodes:
        visited[node[0], node[1]] = True
    for node in nodes:
        for neighbor in get_neighbors(node):
            if not visited[neighbor[0], neighbor[1]]:
                # each of these is a new trail to follow (trail meaning the route from
                # one node tile to another, which will be an edge in the resulting graph)
                current = neighbor
                trail_length = 1
                slope_type = None # will be -1 for against and 1 for with, for the whole trail
                direction = get_direction(neighbor, node) # will be (x, y) with x and y in [-1, 1], just the current moving direction
                while True:
                    trail_length += 1
                    visited[current[0], current[1]] = True
                    if grid[current[0], current[1]] in slopes:
                        slope_type = determine_slope_type(grid[current[0], current[1]], direction)
                    unvisited_neighbor = None
                    for neighbor in get_neighbors(current):
                        if not visited[neighbor[0], neighbor[1]]:
                            unvisited_neighbor = neighbor
                    if unvisited_neighbor is None:
                        # this is the end of the trail, so find which node it is connected to
                        for neighbor in get_neighbors(current):
                            if neighbor in nodes and neighbor != node:
                                other_node = neighbor
                                break
                        add_edge(node, other_node, trail_length, slope_type)
                        break
                    else:
                        # continue
                        direction = get_direction(unvisited_neighbor, current)
                        current = unvisited_neighbor

grid_to_graph()

G = nx.DiGraph(adj)

paths = nx.all_simple_paths(G, 0, 1)

path_lengths = []
for path in paths:
    path_length = 0
    for i in range(len(path[:-1])):
        path_length += adj[path[i], path[i + 1]]
    path_lengths.append(int(path_length))

result = max(path_lengths)
print(result)

# import matplotlib.pyplot as plt
# nx.draw(G, pos=nodes)
# plt.show()