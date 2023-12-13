import numpy as np

with open("day13.txt", "r") as f:
    input = f.read()

lines = input.split("\n")
modules = []
module = ""
for line in lines:
    if len(line) > 0:
        module += line + "\n"
    else:
        modules.append(module[:-1])
        module = ""
modules.append(module[:-1])

grids = []
for module in modules:
    a = np.array([list(i) for i in module.split("\n")])
    grids.append((a == "#").astype(int))


def get_horizontal_mirrors(grid):
    horizontal_mirrors = []
    for i in range(grid.shape[0] - 1):
        size = min(i + 1, grid.shape[0] - i - 1)
        top = grid[max(0, i + 1 - size) : i + 1, :]
        bottom = grid[i + size : i : -1, :]
        diff = top - bottom
        if np.sum(np.abs(diff)) == 1:
            horizontal_mirrors.append(i + 1)
    return horizontal_mirrors


result = 0
for grid in grids:
    hor = get_horizontal_mirrors(grid)
    vert = get_horizontal_mirrors(grid.transpose())
    result += sum(i * 100 for i in hor) + sum(i for i in vert)

print(result)