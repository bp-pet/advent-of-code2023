import numpy as np
import networkx as nx

with open("day17.txt", 'r') as f:
    input = f.read()

# input = "12\n34"

directions = ["r", "l", "u", "d"]

grid = np.array([list(i) for i in input.split("\n")], dtype=int)

# create and add nodes, 13 for each original node:
# no movement, 1 to 3 for each of 4 directions
G = nx.DiGraph()
node_list = []
counter = 0
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        d = {"x": i, "y": j} | {k: 0 for k in directions}
        if i == 0 and j == 0:
            node_list.append((counter, d))
        counter += 1
        for direction in directions:
            for step in range(1, 4):
                temp = dict(d)
                temp[direction] = step
                node_list.append((counter, temp))
                counter += 1
G.add_nodes_from(node_list)

def get_new_node_dict(d: dict, direction: str):
    # get the data representation of given node data if it were
    # to move in a particular direction, regardless whether that
    # direction is legal
    target_node_data = dict(d)
    target_node_data[direction] += 1
    for not_direction in directions:
        if not_direction != direction:
            target_node_data[not_direction] = 0
    if direction == "r":
        target_node_data["y"] += 1
    elif direction == "l":
        target_node_data["y"] -= 1
    if direction == "u":
        target_node_data["x"] -= 1
    if direction == "d":
        target_node_data["x"] += 1
    return target_node_data
    
print("Starting to add edges")
edge_weights = {}
nodes_data = G.nodes(data=True)
# connect each node to each direction, if possible
for direction in directions:
    for source_node_index, source_node_data in enumerate(nodes_data):
        target_node_data = get_new_node_dict(source_node_data[1], direction)
        target_nodes = [n for n,v in G.nodes(data=True) if v == target_node_data]
        if len(target_nodes) == 0:
            # out of bounds or move not possible
            pass
        elif len(target_nodes) > 1:
            raise Exception("Something is wrong")
        else:
            target_node_index = target_nodes[0]
            weight = grid[target_node_data["x"], target_node_data["y"]]
            G.add_edge(source_node_index, target_node_index)
            edge_weights[(source_node_index, target_node_index)] = {"weight": weight}
nx.set_edge_attributes(G, edge_weights)

print(G.nodes(data=True)[0])

start_node_index = 0
target_node_indices = [n for n,v in G.nodes(data=True) if v["x"] == grid.shape[0] - 1 and v["y"] == grid.shape[1] - 1]

# import matplotlib.pyplot as plt
# nx.draw(G)
# plt.show()
# raise Exception

shortest_paths = []
for target_node_index in target_node_indices:
    print("HERE")
    try:
        s = nx.shortest_path_length(G, start_node_index, target_node_index, "weight")
    except:
        continue
    shortest_paths.append(s)

result = min(shortest_paths)
print(result)