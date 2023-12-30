"""
Heuristic method: pick random pairs of nodes and get the shortest path between them.
Record which edges are used every time and keep track of how many times each edge has
occured. This results in the top 3 seen edges being exactly the cut edges. This should not
work on every possible input.

Alternatively one could use a cut-finding method from networkx.
"""

import networkx as nx

with open("day25.txt", "r") as f:
    raw = f.read()

# get components
components = {}
for line in raw.split("\n"):
    temp = line.split(" ")
    components[temp[0][:-1]] = temp[1:]

# make graph
G = nx.Graph()
for component in components:
    G.add_node(component)
for component in components:
    for connection in components[component]:
        G.add_edge(component, connection)
nodes_list = list(G.nodes)

counts = {edge: 0 for edge in G.edges}

import random
for _ in range(10000):
    node1 = random.choice(nodes_list)
    node2 = random.choice(nodes_list)
    path = nx.shortest_path(G, node1, node2)
    for i in range(len(path) - 1):
        try:
            counts[(path[i], path[i + 1])] += 1
        except KeyError:
            counts[(path[i + 1], path[i])] += 1

sorted_edges = [e for e in sorted(counts.items(), key=lambda item: item[1], reverse=True)]


edges_to_remove = [i[0] for i in sorted_edges[:3]]

for edge in edges_to_remove:
    G.remove_edge(edge[0], edge[1])

connected_components = nx.connected_components(G)

sizes = []
for c in connected_components:
    sizes.append(len(c))

if len(sizes) != 2:
    raise Exception("Removing given edges results in more or less than 2 components")

result = sizes[0] * sizes[1]
print(result)