import numpy as np

with open("day14.txt", 'r') as f:
    input = f.read()

grid = np.array([list(i) for i in input.split("\n")])

result = 0

def slide_north():
    for col in range(grid.shape[1]):
        support = 0
        for row in range(grid.shape[0]):
            c = grid[row, col]
            if c == ".":
                pass
            elif c == "#":
                support = row + 1
            elif c == "O":
                new_row = support
                support += 1
                if row != new_row:
                    grid[row, col] = "."
                    grid[new_row, col] = "O"

def calculate_load():
    result = 0
    for col in range(grid.shape[1]):
        for row in range(grid.shape[0]):
            if grid[row, col] == "O":
                result += grid.shape[0] - row
    return result

def get_binary_grid():
    return grid == "O"

def check_if_array_is_seen(a):
    for i, s in enumerate(seen):
        if (a == s).all():
            return i
    return None


seen = [get_binary_grid()]

n = 1000000000

for i in range(n):
    for j in range(4):
        slide_north()
        grid = np.rot90(grid, k=3)
    binary = get_binary_grid()
    is_seen = check_if_array_is_seen(binary)
    if is_seen is not None:
        cycle_size = i - is_seen + 1
        iterations_done = i
        break
    seen = np.concatenate([seen, [np.array(binary)]])

for i in range((n - iterations_done - 1) % cycle_size):
    for j in range(4):
        slide_north()
        grid = np.rot90(grid, k=3)

result = calculate_load()