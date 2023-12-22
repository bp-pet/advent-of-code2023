import numpy as np

with open("day21.txt", "r") as f:
    input = f.read()

grid = np.array([list(i) for i in input.split("\n")])

S = tuple(np.argwhere(grid == "S")[0])

number_of_steps = 64

is_saved = np.zeros(grid.shape + tuple([number_of_steps + 1]), dtype=bool)

reachable = np.zeros_like(grid, dtype=bool)

def find_available_neighbors(pos):
    result = []
    for i in [-1, 1]:
        new_x = pos[0] + i
        if new_x < 0 or new_x >= grid.shape[0]:
            continue
        if grid[new_x, pos[1]] != "#":
            result.append((new_x, pos[1]))
    for j in [-1, 1]:
        new_y = pos[1] + j
        if new_y < 0 or new_y >= grid.shape[1]:
            continue
        if grid[pos[0], new_y] != "#":
            result.append((pos[0], new_y))
    return result


def search(start_pos, steps_left):
    if is_saved[start_pos[0], start_pos[1], steps_left]:
        return
    else:
        if steps_left == 0:
            reachable[start_pos] = True
        else:
            for neighbor in find_available_neighbors(start_pos):
                search(neighbor, steps_left - 1)
        is_saved[start_pos[0], start_pos[1], steps_left] = True
    
def reachable_to_string():
    result = ""
    for i in range(reachable.shape[0]):
        for j in range(reachable.shape[1]):
            if reachable[i, j]:
                result += "O"
            else:
                result += grid[i, j]
        result += "\n"
    return result[:-1]

def count_reachable():
    return len(np.argwhere(reachable))

search(S, number_of_steps)

# print(reachable_to_string())

print(count_reachable())