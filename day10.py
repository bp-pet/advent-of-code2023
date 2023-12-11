with open("day10.txt", 'r') as f:
    input = f.read()

grid = [list(i) for i in input.split("\n")]

legend = {'-': ('l', 'r'),
          '|': ('u', 'd'),
          'J': ('l', 'u'),
          'L': ('r', 'u'),
          'F': ('d', 'r'),
          '7': ('d', 'l'),
          '.': ()}

def find_start():
    for i, a in enumerate(grid):
        for j, b in enumerate(a):
            if b == "S":
                return (i, j)

start_pos = find_start()

def check_pos_valid(pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[0]):
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
    while True:
        distance += 1
        current_pos = calculate_new_pos(current_pos, current_dir)
        if not check_pos_valid(current_pos):
            # if next pos is out of bounds, stop
            return 0
        if current_pos == start_pos:
            # if start reached, we are done
            return distance // 2
        if get_opposite_dir(current_dir) not in legend[get_tile(current_pos)]:
            # if next pos does not have appropriate incoming direction, stop
            return 0
        current_dir = get_new_dir(current_dir, get_tile(current_pos))

def find_result():
    for d in ['u', 'd', 'r', 'l']:
        outcome = check_start_dir(d)
        if outcome:
            return outcome

result = find_result()
print(result)