import numpy as np
import networkx as nx

with open("day17.txt", 'r') as f:
    input = f.read()

# input = "12\n34"

directions = [0, 1, 2, 3]  # ["r", "l", "u", "d"]

grid = np.array([list(i) for i in input.split("\n")], dtype=int)

# create and add nodes, 12 for each original node (except first with 13):
# 1 to 3 for each of 4 directions
G = nx.DiGraph()
node_list = []
counter = 0
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        d = [i, j, 0, 0, 0, 0]
        if i == 0 and j == 0:
            node_list.append(tuple(d))
        counter += 1
        for direction in directions:
            for step in range(1, 4):
                temp = list(d)
                temp[2 + direction] = step
                node_list.append(tuple(temp))
                counter += 1
G.add_nodes_from(node_list)
print("Finished adding nodes")

def get_target_node(source_node: tuple, direction: int):
    # get the data representation of given node data if it were
    # to move in a particular direction, regardless whether that
    # direction is legal
    target_node = list(source_node)
    target_node[2 + direction] += 1
    for not_direction in directions:
        if not_direction != direction:
            target_node[2 + not_direction] = 0
    if direction == 0:
        target_node[1] += 1
    elif direction == 1:
        target_node[1] -= 1
    if direction == 2:
        target_node[0] -= 1
    if direction == 3:
        target_node[0] += 1
    target_node = tuple(target_node)
    return target_node

# connect each node to each direction, if possible
for direction in directions:
    for source_node in G.nodes:
        if (source_node[2 + 0] and direction == 1) or (source_node[2 + 1] and direction == 0) or (source_node[2 + 2] and direction == 3) or (source_node[2 + 3] and direction == 2):
            # make sure going in opposite direction is not possible
            continue
        target_node = get_target_node(source_node, direction)
        if target_node not in G.nodes:
            # out of bounds or move not possible
            pass
        else:
            weight = grid[target_node[0], target_node[1]]
            G.add_edge(source_node, target_node, weight=weight)
print("Finished adding edges")

# add start and end nodes
start_node_name = "start"
finish_node_name = "finish"
G.add_node(start_node_name)
target_node = (0, 0, 0, 0, 0, 0)
G.add_edge(start_node_name, target_node, weight=0)
G.add_node(finish_node_name)
for direction in directions:
    for value in range(1, 4):
        source_node = [grid.shape[0] - 1, grid.shape[1] - 1, 0, 0, 0, 0]
        source_node[2 + direction] = value
        source_node = tuple(source_node)
        G.add_edge(source_node, finish_node_name, weight=0)
print("Finished adding start and end")

result = nx.shortest_path_length(G, start_node_name, finish_node_name, "weight")
print(result)

# path = nx.shortest_path(G, start_node_name, finish_node_name, "weight")
# grid = np.array(grid, dtype=str)
# for p in path[1:-1]:
#     grid[p[0], p[1]] = "x"
# s = ""
# for i in range(grid.shape[0]):
#     for j in range(grid.shape[1]):
#         s += grid[i, j]
#     s += "\n"

# print(path)
# print(s)
# print(grid.shape)
# test_node = (grid.shape[0] - 2, grid.shape[1] - 1, 0, 0, 0, 3)
# print(test_node)
# out_edges = G.out_edges(test_node)
# for out_edge in out_edges:
#     print("  ", out_edge[1])