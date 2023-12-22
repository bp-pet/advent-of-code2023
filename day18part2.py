import numpy as np

with open("day18demo.txt", "r") as f:
    input = f.read()

lines = input.split("\n")

directions = []

hex_dir_dict = {0: "R", 1: "D", 2: "L", 3: "U"}

for line in lines:
    hex = line.split(" ")[2][1:-1]
    print(hex)
    distance = int(hex[1:6], 16)
    direction = hex_dir_dict[int(hex[6])]
    directions.append((direction, distance))

current_pos = [0, 0]
max_x = 0
min_x = 0
max_y = 0
min_y = 0
for direction in directions:
    if direction[0] == "R":
        current_pos[1] += direction[1]
    elif direction[0] == "L":
        current_pos[1] -= direction[1]
    elif direction[0] == "U":
        current_pos[0] -= direction[1]
    elif direction[0] == "D":
        current_pos[0] += direction[1]
    else:
        raise Exception("Problem")
    if current_pos[0] > max_x:
        max_x = current_pos[0]
    if current_pos[0] < min_x:
        min_x = current_pos[0]
    if current_pos[1] > max_y:
        max_y = current_pos[1]
    if current_pos[1] < min_y:
        min_y = current_pos[1]

x_size = max_x - min_x + 1
y_size = max_y - min_y + 1

grid = np.zeros([x_size, y_size])
current_pos = [-min_x, -min_y]

grid[current_pos[0], current_pos[1]] = 1
for direction in directions:
    x_grow = 0
    y_grow = 0
    if direction[0] == "R":
        for i in range(direction[1]):
            current_pos[1] += 1
            grid[current_pos[0], current_pos[1]] = 1
    elif direction[0] == "L":
        for i in range(direction[1]):
            current_pos[1] -= 1
            grid[current_pos[0], current_pos[1]] = 1
    elif direction[0] == "U":
        for i in range(direction[1]):
            current_pos[0] -= 1
            grid[current_pos[0], current_pos[1]] = 1
    elif direction[0] == "D":
        for i in range(direction[1]):
            current_pos[0] += 1
            grid[current_pos[0], current_pos[1]] = 1
    else:
        raise Exception("Problem")


def show_grid():
    result = ""
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            result += "#" if grid[i, j] else "."
        result += "\n"
    return result[:-1]

grid = np.concatenate([np.zeros([grid.shape[0], 1]), grid, np.zeros([grid.shape[0], 1])], axis=1)
grid = np.concatenate([np.zeros([1, grid.shape[1]]), grid, np.zeros([1, grid.shape[1]])], axis=0)

# with open("test.txt", 'w') as f:
#     f.write(show_grid())

print(grid.shape)

raise Exception

visited = np.zeros_like(grid)

def is_valid_pos(pos):
    if pos[0] < 0 or pos[0] >= grid.shape[0]:
        return False
    if pos[1] < 0 or pos[1] >= grid.shape[1]:
        return False
    return True

def find_full_area(i, j):
    area = [(i, j)]
    queue = [(i, j)]
    visited[i, j] = True
    while len(queue) > 0:
        current = queue.pop(0)
        for i in [-1, 1]:
            next = (current[0] + i, current[1])
            if is_valid_pos(next) and not visited[next] and not grid[next]:
                visited[next] = 1
                queue.append(next)
                area.append(next)
        for j in [-1, 1]:
            next = (current[0], current[1] + j)
            if is_valid_pos(next) and not visited[next] and not grid[next]:
                visited[next] = 1
                queue.append(next)
                area.append(next)
    return len(area)

outside = find_full_area(0, 0)
path = len(np.argwhere(grid))
total = grid.shape[0] * grid.shape[1]
inside = total - outside - path
print("total", total, "should be", 108)
print("path", path, "should be", 38)
print("outside", outside, "should be", 46)
print("inside", inside)
print("final answer", inside + path)