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
    grids.append(np.array([list(i) for i in module.split("\n")]))


def get_horizontal_mirrors(grid):
    horizontal_mirrors = []
    for i in range(grid.shape[0] - 1):
        flag = True
        top = i
        bottom = i + 1
        while top >= 0 and bottom < grid.shape[0]:
            if (grid[top, :] != grid[bottom, :]).any():
                flag = False
                break
            top -= 1
            bottom += 1
        if flag:
            horizontal_mirrors.append(i + 1)
    return horizontal_mirrors

def get_vertical_mirrors(grid):
    vertical_mirrors = []
    for j in range(grid.shape[1] - 1):
        flag = True
        left = j
        right = j + 1
        while left >= 0 and right < grid.shape[1]:
            if (grid[:, left] != grid[:, right]).any():
                flag = False
                break
            left -= 1
            right += 1
        if flag:
            vertical_mirrors.append(j + 1)
    return vertical_mirrors

result = 0
for grid in grids:
    hor = get_horizontal_mirrors(grid)
    vert = get_vertical_mirrors(grid)
    result += sum(i * 100 for i in hor) + sum(i for i in vert)

print(result)