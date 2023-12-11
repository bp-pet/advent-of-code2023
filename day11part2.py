with open("day11.txt", 'r') as f:
    input = f.read()

lines = input.split("\n")

grid = []
for line in lines:
    grid.append(list(line))

size_x = len(grid)
size_y = len(grid[0])

empty_rows = []
empty_cols = []

for i in range(size_x):
    found = False
    for j in range(size_y):
        if grid[i][j] == "#":
            found = True
            break
    if not found:
        empty_rows.append(i)

for j in range(size_y):
    found = False
    for i in range(size_x):
        if grid[i][j] == "#":
            found = True
            break
    if not found:
        empty_cols.append(j)

# for r in empty_rows[::-1]:
#     grid.insert(r, ["."] * size_y)
# size_x += len(empty_rows)
# for c in empty_cols[::-1]:
#     for i in range(size_x):
#         grid[i].insert(c, ".")
# size_y += len(empty_cols)

stars = []
for i in range(size_x):
    for j in range(size_y):
        if grid[i][j] == "#":
            stars.append((i, j))

def is_number_between_numbers(x, a, b):
    # check if x is between a and b
    return (x - a) * (b - x) > 0

multiplier = 1000000

result = 0
for s1 in stars:
    for s2 in stars:
        if s1 == s2:
            continue
        empty_rows_passed = 0
        for r in empty_rows:
            if is_number_between_numbers(r, s1[0], s2[0]):
                empty_rows_passed += 1
        empty_cols_passed = 0
        for c in empty_cols:
            if is_number_between_numbers(c, s1[1], s2[1]):
                empty_cols_passed += 1
        x_dist = abs(s1[0] - s2[0]) + (empty_rows_passed * (multiplier - 1))
        y_dist = abs(s1[1] - s2[1]) + (empty_cols_passed * (multiplier - 1))
        result += x_dist + y_dist

result = result // 2
print(result)