import numpy as np
import networkx as nx

number_of_steps_allowed = 26501365

with open("day21.txt", "r") as f:
    input = f.read()

grid = np.array([list(i) for i in input.split("\n")])
S = tuple(np.argwhere(grid == "S")[0])

# we need the dimensions of the grid to be odd
assert grid.shape[0] % 2 == 1
assert grid.shape[1] % 2 == 1
assert number_of_steps_allowed % 2 == 1

# make graph
graph = nx.Graph()
for row in range(grid.shape[0]):
    for col in range(grid.shape[1]):
        if grid[row, col] != "#":
            if row < grid.shape[0] - 1 and grid[row + 1, col] != "#":
                graph.add_edge(f"{row}, {col}", f"{row + 1}, {col}")
            if col < grid.shape[1] - 1 and grid[row, col + 1] != "#":
                graph.add_edge(f"{row}, {col}", f"{row}, {col + 1}")

# define entrances: top left, top mid, top right, etc (including center)
vertical_entrance_coords = {0: 0, 1: grid.shape[0] // 2, 2: grid.shape[0] - 1}
horizontal_entrance_coords = {0: 0, 1: grid.shape[1] // 2, 2: grid.shape[1] - 1}

# precalculate important values
steps_to_cover_chunk = np.zeros((3, 3), dtype=np.int64)
coverable_spots_even = np.zeros_like(steps_to_cover_chunk)
coverable_spots_odd = np.zeros_like(steps_to_cover_chunk)
shortest_path_lengths = {}
for row in range(3):
    for col in range(3):
        entrance_coords = (vertical_entrance_coords[row], horizontal_entrance_coords[col])
        sp_dict = nx.shortest_path_length(graph, f"{entrance_coords[0]}, {entrance_coords[1]}")
        shortest_path_lengths[(row, col)] = sp_dict
        steps_to_cover_chunk[row, col] = max(sp_dict.values())
        for s in sp_dict.values():
            if s % 2 == 0:
                coverable_spots_even[row, col] += 1
            else:
                coverable_spots_odd[row, col] += 1

# set up lookup dict for finding how many are reachable in different scenarios
coverable_lookup = {}

def get_distance_to_start_of_chunk(i, j):
    if i == 0 and j == 0:
        return 0
    elif j == 0:
        return (abs(i) - 1) * grid.shape[0] + grid.shape[0] // 2 + 1
    elif i == 0:
        return (abs(j) - 1) * grid.shape[1] + grid.shape[1] // 2 + 1
    else:
        return (abs(i) - 1) * grid.shape[0] + grid.shape[0] // 2 + 1 + (abs(j) - 1) * grid.shape[1] + grid.shape[1] // 2 + 1

def get_entrance_index_of_chunk(i, j):
    if i == 0 and j == 0:
        entrance_index = (1, 1)
    elif i == 0 and j > 0:
        entrance_index = (1, 0)
    elif i == 0 and j < 0:
        entrance_index = (1, 2)
    elif i > 0 and j == 0:
        entrance_index = (2, 1)
    elif i > 0 and j > 0:
        entrance_index = (2, 0)
    elif i > 0 and j < 0:
        entrance_index = (2, 2)
    elif i < 0 and j == 0:
        entrance_index = (0, 1)
    elif i < 0 and j > 0:
        entrance_index = (0, 0)
    elif i < 0 and j < 0:
        entrance_index = (0, 2)
    return entrance_index

def get_steps_needed_to_cover_chunk(i, j):
    entrance = get_entrance_index_of_chunk(i, j)
    return steps_to_cover_chunk[entrance[0], entrance[1]]

def is_reachable(i, j):
    return number_of_steps_allowed >= get_distance_to_start_of_chunk(i, j)

def get_partially_coverable(entrance_index, steps_left):
    if (entrance_index, steps_left) in coverable_lookup:
        return coverable_lookup[(entrance_index, steps_left)]
    shortest_paths = shortest_path_lengths[(entrance_index[0], entrance_index[1])]
    counter = 0
    for s in shortest_paths.values():
        diff = steps_left - s
        if diff >= 0 and diff % 2 == 0:
            counter += 1
    coverable_lookup[(entrance_index, steps_left)] = counter
    return counter

def get_coverable_in_chunk(i, j):
    if not is_reachable(i, j):
        return 0
    steps_left = number_of_steps_allowed - get_distance_to_start_of_chunk(i, j)
    entrance = get_entrance_index_of_chunk(i, j)
    if get_steps_needed_to_cover_chunk(i, j) <= steps_left:
        # fully coverable
        if steps_left % 2 == 0:
            return coverable_spots_even[entrance[0], entrance[1]]
        else:
            return coverable_spots_odd[entrance[0], entrance[1]]
    else:
        return get_partially_coverable(entrance, steps_left)

def lowest_row_to_check(j):
    tolerance = 5
    horizontal_steps_taken = max(0, (abs(j) - 1) * grid.shape[1] + grid.shape[1] // 2 + 1)
    vertical_steps_left = number_of_steps_allowed - horizontal_steps_taken
    return max(0, vertical_steps_left // grid.shape[0] - tolerance)

def get_covered_from_skipped_chunks(i, j):
    """
    Automatically get all coverable squares of chunk column j for rows up to
    (not including) i.
    """
    if i == 0:
        return 0
    
    result = 0
    nonneg_row = (i >= 0)
    i = abs(i) - 1
    number_of_even_chunks = i // 2
    number_of_odd_chunks = i // 2 if i % 2 == 0 else i // 2 + 1

    # if col is even, switch counts
    if j % 2 == 0:
        number_of_even_chunks, number_of_odd_chunks = number_of_odd_chunks, number_of_even_chunks

    # all have the same entrance except for row 0
    entrance = get_entrance_index_of_chunk(i, j)
    result += number_of_even_chunks * coverable_spots_even[entrance[0], entrance[1]]
    result += number_of_odd_chunks * coverable_spots_odd[entrance[0], entrance[1]]
    
    # if we are on the nonnegative row side, include a count row 0 as well
    if nonneg_row:
        if j % 2 == 0:
            result += coverable_spots_odd[1, entrance[1]]
        else:
            result += coverable_spots_even[1, entrance[1]]
    
    return result

def count_all():
    count = 0
    for col_increment in [1, -1]:
        col = 0 if col_increment == 1 else -1
        while True:
            column_has_changes = False
            for row_increment in [1, -1]:
                row = row_increment * lowest_row_to_check(col)
                if row_increment == -1:
                    # if going downwards, always skip 0
                    row = min(row, -1)
                count += get_covered_from_skipped_chunks(row, col)
                while True:
                    coverable = get_coverable_in_chunk(row, col)
                    if coverable:
                        column_has_changes = True
                        count += coverable
                        row += row_increment
                    else:
                        break
            if not column_has_changes:
                break
            col += col_increment

result = count_all()
print(result)