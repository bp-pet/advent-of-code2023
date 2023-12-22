import math
import numpy as np

with open("day17demo.txt", 'r') as f:
    input = f.read()

input = "123\n456\n789\n987\n123"

grid = np.array([list(i) for i in input.split("\n")], dtype=int)
x_size = grid.shape[0]
y_size = grid.shape[1]

source = [0, 0]
target = [x_size - 1, y_size - 1]

distances_grid = np.ones_like(grid) * math.inf
distances_grid[0, 0] = 0

previous_grid = np.ones_like(grid, dtype=tuple)
for i in range(x_size):
    for j in range(y_size):
        previous_grid[i, j] = None

queue = []
for i in range(x_size):
    for j in range(y_size):
        queue.append((i, j))

def find_min_dist():
    found_min = math.inf
    found_min_v = None
    found_min_v_index = None
    for i, v in enumerate(queue):
        if grid[v[0], v[1]] < found_min:
            found_min = grid[v[0], v[1]]
            found_min_v = v
            found_min_v_index = i
    return found_min_v, found_min_v_index

while len(queue) > 0:
    u, i = find_min_dist()
    if u == target:
        break
    queue.pop(i)

    print(f"chosen u {u}")

    for v in queue:
        if abs(u[0] - v[0]) + abs(u[1] - v[1]) != 1:
            continue
        print(f"neighbor {v}")
        alt = distances_grid[u[0], u[1]] + grid[v[0], v[1]]
        if alt < distances_grid[v[0], v[1]]:
            print(f"updating {v} to {alt}")
            distances_grid[v[0], v[1]] = alt
            previous_grid[v[0], v[1]] = u

print(distances_grid)