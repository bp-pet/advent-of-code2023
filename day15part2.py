from collections import OrderedDict

with open("day15.txt", 'r') as f:
    input = f.read()

commands = input.split(",")

def string_to_hash(string):
    hash = 0
    for c in string:
        hash = ((hash + ord(c)) * 17) % 256
    return hash

boxes = []
for i in range(256):
    boxes.append(OrderedDict())

for command in commands:
    if len(command.split("-")) == 1:
        # equals
        lens_hash = command[:-2]
        lens_strength = int(command[-1])
        target_box_index = string_to_hash(lens_hash)
        boxes[target_box_index][lens_hash] = lens_strength
    else:
        # minus
        lens_hash = command[:-1]
        target_box_index = string_to_hash(lens_hash)
        if lens_hash in boxes[target_box_index]:
            del boxes[target_box_index][lens_hash]

result = 0
for box_index, box in enumerate(boxes):
    for lens_index, lens_hash in enumerate(box):
        lens_strength = box[lens_hash]
        result += (box_index + 1) * (lens_index + 1) * lens_strength
print(result)