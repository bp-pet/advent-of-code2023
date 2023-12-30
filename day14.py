import numpy as np

with open("day14.txt", 'r') as f:
    input = f.read()

grid = np.array([list(i) for i in input.split("\n")])


result = 0

for col in range(grid.shape[1]):
    support = 0
    for row in range(grid.shape[0]):
        c = grid[row, col]
        if c == ".":
            pass
        elif c == "#":
            support = row + 1
        elif c == "O":
            support += 1
            result += grid.shape[1] - support + 1

print(result)