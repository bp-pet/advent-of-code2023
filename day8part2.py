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
            if checkpoint in checkpoints:
                if len(checkpoints) > 1:
                    raise Exception("Something is wrong")
                break
            checkpoints.append(checkpoint)
        direction = directions[direction_index]
        if direction == "L":
            p = modules[p][0]
        else:
            p = modules[p][1]
        move_counter += 1
    vals.append(move_counter // 2)

print(vals)

from math import gcd
lcm = 1
for i in vals:
    lcm = lcm*i//gcd(lcm, i)
print(lcm)



# while set(current_pos) != set(targets):
#     direction = directions[move_counter % len(directions)]

#     for i, p in enumerate(current_pos):
#         if direction == "L":
#             current_pos[i] = modules[current_pos[i]][0]
#         else:
#             current_pos[i] = modules[current_pos[i]][1]
#     move_counter += 1

# print(move_counter)