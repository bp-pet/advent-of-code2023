from math import gcd

with open("day8.txt", 'r') as f:
    input = f.read()

lines = input.split("\n")

directions = lines[0]
modules_str = lines[2:]

# process modules
modules = {}
for module_str in modules_str:
    temp = module_str.split(" ")
    modules[temp[0]] = (temp[2][1:4], temp[3][0:3])

current_pos = []
targets = []

for module in modules:
    if module[-1] == "A":
        current_pos.append(module)
    elif module[-1] == "Z":
        targets.append(module)

vals = []
for p in current_pos:
    move_counter = 0
    checkpoints = []
    while True:
        direction_index = move_counter % len(directions)
        if p[2] == "Z":
            checkpoint = (p, direction_index)
            # assume each starting module reaches only one target module and always at the end of the move list
            if checkpoint in checkpoints:
                if len(checkpoints) > 1:
                    raise Exception("Multiple target modules reached from one starting module, so solution is not valid")
                break
            checkpoints.append(checkpoint)
        direction = directions[direction_index]
        if direction == "L":
            p = modules[p][0]
        else:
            p = modules[p][1]
        move_counter += 1
    vals.append(move_counter // 2)

# find lcm of vals
result = 1
for i in vals:
    result = result*i//gcd(result, i)
print(result)