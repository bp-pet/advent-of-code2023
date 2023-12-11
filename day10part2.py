with open("day10.txt", 'r') as f:
    input = f.read()

grid = [list(i) for i in input.split("\n")]

size_x = len(grid)
size_y = len(grid[0])
original_area = size_x * size_y

legend = {'-': ('l', 'r'),
          '|': ('u', 'd'),
          'J': ('l', 'u'),
          'L': ('r', 'u'),
          'F': ('d', 'r'),
          '7': ('d', 'l'),
          '.': ()}

def find_start():
    for i in range(size_x):
        for j in range(size_y):
            if grid[i][j] == "S":
                return (i, j)

start_pos = find_start()

def check_pos_valid(pos):
    if pos[0] < 0 or pos[0] >= size_x:
        return False
    if pos[1] < 0 or pos[1] >= size_y:
        return False
    return True

def calculate_new_pos(pos, d):
    if d == 'u':
        return (pos[0] - 1, pos[1])
    elif d == 'd':
        return (pos[0] + 1, pos[1])
    elif d == 'l':
        return (pos[0], pos[1] - 1)
    elif d == 'r':
        return(pos[0], pos[1] + 1)

def get_opposite_dir(d):
    if d == 'u':
        return 'd'
    elif d == 'd':
        return 'u'
    elif d == 'l':
        return 'r'
    elif d == 'r':
        return 'l'
    else:
        raise Exception("Something is wrong")

def get_new_dir(old_dir, tile):
    """
    Previous move was in direction old_dir, arriving at tile.
    """
    arrival_dir = get_opposite_dir(old_dir)
    dirs = legend[tile]
    if arrival_dir == dirs[0]:
        return dirs[1]
    elif arrival_dir == dirs[1]:
        return dirs[0]
    else:
        raise Exception("Something is wrong")

def get_tile(pos):
    return grid[pos[0]][pos[1]]

def check_start_dir(d):
    current_pos = start_pos
    current_dir = d
    distance = 0
    path = [current_pos]
    path_dirs = [current_dir]
    while True:
        distance += 1
        current_pos = calculate_new_pos(current_pos, current_dir)
        if not check_pos_valid(current_pos):
            # if next pos is out of bounds, stop
            return 0
        if current_pos == start_pos:
            # if start reached, we are done
            return path, path_dirs
        if get_opposite_dir(current_dir) not in legend[get_tile(current_pos)]:
            # if next pos does not have appropriate incoming direction, stop
            return 0
        current_dir = get_new_dir(current_dir, get_tile(current_pos))
        path.append(current_pos)
        path_dirs.append(current_dir)


def find_result():
    for d in ['u', 'd', 'r', 'l']:
        outcome = check_start_dir(d)
        if outcome:
            return outcome

path, path_dirs = find_result()

def grid_to_str(grid):
    result = ""
    for i in grid:
        for j in i:
            result += j
        result += "\n"
    return result [:-1]

path_grid = []
for i in range(size_x):
    path_grid.append([False] * size_y)
for i, p in enumerate(path):
    path_grid[p[0]][p[1]] = path_dirs[i]

areas = []

visited = []
for i in range(size_x):
    visited.append([False] * size_y)
for p in path:
    visited[p[0]][p[1]] = True

def check_if_visited(pos):
    return visited[pos[0]][pos[1]]

def check_if_path(pos):
    return path_grid[pos[0]][pos[1]]

def get_approach_type(incoming_dir, flow_dir):
    if incoming_dir == 'd':
        if flow_dir == 'r':
            return 0
        elif flow_dir == 'l':
            return 1
        else:
            raise Exception("This is not good")
    elif incoming_dir == 'u':
        if flow_dir == 'r':
            return 1
        elif flow_dir == 'l':
            return 0
        else:
            raise Exception("This is not good")
    elif incoming_dir == 'r':
        if flow_dir == 'u':
            return 0
        elif flow_dir == 'd':
            return 1
        else:
            raise Exception("This is not good")
    elif incoming_dir == 'l':
        if flow_dir == 'u':
            return 1
        elif flow_dir == 'd':
            return 0
        else:
            raise Exception("This is not good")

def find_full_area(i, j):
    area = [(i, j)]
    queue = [(i, j)]
    visited[i][j] = True
    approach = None
    while len(queue) > 0:
        current = queue.pop(0)
        for d in ['u', 'd', 'r', 'l']:
            next = calculate_new_pos(current, d)
            if check_pos_valid(next):
                if check_if_path(next):
                    path_dir = path_grid[next[0]][next[1]]
                    try:
                        if approach is None:
                            approach = get_approach_type(d, path_dir)
                        else:
                            if approach != get_approach_type(d, path_dir):
                                print("PROBLEM")
                    except:
                        pass
                else:
                    if not check_if_visited(next):
                        area.append(next)
                        queue.append(next)
                        visited[next[0]][next[1]] = True
    return area, approach

areas = []
for i in range(size_x):
    for j in range(size_y):
        if not visited[i][j]:
            area, approach = find_full_area(i, j)
            areas.append((area, approach))

def check_if_ground(pos):
    return grid[pos[0]][pos[1]] == '.'

sums = {0: 0, 1: 0, 'Don\'t know': 0}
for area in areas:
    positions = area[0]
    approach_type = area[1]
    if approach_type is not None:
        sums[approach_type] += len(positions)
    else:
        sums['Don\'t know'] += len(positions)

print(sums)

##################################

# basically blow up the grid, adding an artificial row and column between the
# existing ones; most code before this is useless
new_grid = []
for i in range(size_x * 2 - 1):
    new_grid.append(['@'] * (size_y * 2 - 1))
for i in range(size_x):
    for j in range(size_y):
        new_grid[i * 2][j * 2] = '.'
for p in path:
    new_grid[p[0] * 2][p[1] * 2] = 'x'
for i, p in enumerate(path[:-1]):
    current = (p[0] * 2, p[1] * 2)
    next = (path[i + 1][0] * 2, path[i + 1][1] * 2)
    diff = (next[0] - current[0], next[1] - current[1])
    new = (current[0] + diff[0] // 2, current[1] + diff[1] // 2)
    new_grid[new[0]][new[1]] = 'x'
p = path[-1]
i = -1
current = (p[0] * 2, p[1] * 2)
next = (path[i + 1][0] * 2, path[i + 1][1] * 2)
diff = (next[0] - current[0], next[1] - current[1])
new = (current[0] + diff[0] // 2, current[1] + diff[1] // 2)
new_grid[new[0]][new[1]] = 'x'

# print(grid_to_str(new_grid))

grid = new_grid
size_x = len(grid)
size_y = len(grid[0])

def check_if_path_new(pos):
    return new_grid[pos[0]][pos[1]] == 'x'

visited = []
for i in range(size_x):
    visited.append([False] * size_y)
for i in range(size_x):
    for j in range(size_y):
        if check_if_path_new((i, j)):
            visited[i][j] = True
def check_if_visited_new(pos):
    return visited[pos[0]][pos[1]]


def find_outside_dots():
    i, j = 0, 0
    area = [(i, j)]
    queue = [(i, j)]
    visited[i][j] = True
    approach = None
    counter = 0
    while len(queue) > 0:
        current = queue.pop(0)
        if grid[current[0]][current[1]] == '.':
            counter += 1
        for d in ['u', 'd', 'r', 'l']:
            next = calculate_new_pos(current, d)
            if check_pos_valid(next) and not check_if_path_new(next) and not check_if_visited_new(next):
                area.append(next)
                queue.append(next)
                visited[next[0]][next[1]] = True
    return counter

outside = find_outside_dots()
result = original_area - outside - len(path)

print(result)