with open("day8.txt", 'r') as f:
    input = f.read()

lines = input.split("\n")

directions = lines[0]
modules_str = lines[2:]

current_pos = "AAA"
target = "ZZZ"

# process modules
modules = {}
for module_str in modules_str:
    temp = module_str.split(" ")
    modules[temp[0]] = (temp[2][1:4], temp[3][0:3])

move_counter = 0

while current_pos != target:
    direction = directions[move_counter % len(directions)]
    if direction == "L":
        current_pos = modules[current_pos][0]
    else:
        current_pos = modules[current_pos][1]
    move_counter += 1

print(move_counter)