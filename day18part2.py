"""
The idea is that instead of considering the border as having thickness 1 and dealing
with that while scanning it later, we consider it as having thickness 0, calculate
the area inside it, then add the remaining area along the edges separately;
- for each straight border tile adds half a unit of area
- each inside/interior/convex corner adds 3/4 of an area unit
- each outside/exterior/concave corner adds 1/4 of an area unit
On a simple square we can see the fact that the number of inside corners is always
4 larger than the number of outside corners (a square has 4 inside and 0 outside corners).
Using this knowledge, we can just use the total number of corners, which we know from the
input, to figure out how many corners of each type there are.

For the actual area calculation, we scan the structure from top down, each time collapsing
the top-most border to the next one below it, adding the area. This requires considering
a few cases.
"""

# get directions from input
with open("day18.txt", "r") as f:
    input = f.read()
lines = input.split("\n")
directions = []
hex_dir_dict = {0: "R", 1: "D", 2: "L", 3: "U"}
for line in lines:
    hex = line.split(" ")[2][1:-1]
    distance = int(hex[1:6], 16)
    direction = hex_dir_dict[int(hex[6])]
    directions.append((direction, distance))

# find corners
current_pos = [0, 0]
corners = []
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
    corner = tuple(current_pos)
    corners.append(corner)

# count borders and corners:
straight_border_count = 0
outside_corner_count = (len(directions) - 4) // 2
inside_corner_count = outside_corner_count + 4
for direction in directions:
    straight_border_count += direction[1] - 1
area = int(0.75 * inside_corner_count + 0.25 * outside_corner_count + 0.5 * straight_border_count)

# makes sure that 0 is on same height with 1, 2 with 3, etc
if directions[0][0] in ["R", "L"]:
    corners = [corners[-1]] + corners[:-1]

class Pair:
    """Simply a pair of corners, which are connected in the path by a horizontal
    line. Can be identified by one height (of both corners) and the two horizontal
    coordinates of the corners."""

    def __init__(self, height, end1, end2):
        self.height = height
        if end1 < end2:
            self.left, self.right = end1, end2
        else:
            self.left, self.right = end2, end1
    
    def __str__(self):
        return f"Pair with height {self.height} from {self.left} to {self.right}"

# make pairs of corners on the same height
pairs = []
for i in range(len(corners) // 2):
    height = corners[2 * i][0]
    end1 = corners[2 * i][1]
    end2 = corners[2 * i + 1][1]
    pairs.append(Pair(height, end1, end2))
pairs.sort(key=lambda x: x.height)

# add the area scanning from top down
while len(pairs) > 1:
    top = pairs.pop(0)
    for i, bottom in enumerate(pairs):
        # find the first pair which is below current and not outside of it
        left_outside = not (top.left <= bottom.left <= top.right)
        right_outside = not (top.left <= bottom.right <= top.right)
        left_on = (bottom.left in [top.left, top. right])
        right_on = (bottom.right in [top.left, top. right])
        if left_outside and right_outside:
            # unrelated case
            continue
        bottom = pairs.pop(i)
        break
    if left_outside or right_outside:
        # towards outside case
        if left_outside:
            new_pairs = [Pair(bottom.height, bottom.left, top.right)]
        else:
            new_pairs = [Pair(bottom.height, top.left, bottom.right)]
    elif right_on and left_on:
        # rectangle case
        new_pairs = []
    elif (not right_on) and (not left_on):
        # between case
        new_pairs = [Pair(bottom.height, top.left, bottom.left),
                     Pair(bottom.height, bottom.right, top.right)]
    else:
        # towards inside case
        if left_on:
            new_pairs = [Pair(bottom.height, bottom.right, top.right)]
        else:
            new_pairs = [Pair(bottom.height, bottom.left, top.left)]
    area += (bottom.height - top.height) * (top.right - top.left)
    for new_pair in new_pairs:
        index_to_insert = 0
        for i in range(len(pairs)):
            if new_pair.height <= pairs[i].height:
                index_to_insert = i
                break
        pairs.insert(index_to_insert, new_pair)

print(area)