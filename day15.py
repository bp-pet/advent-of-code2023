with open("day15.txt", 'r') as f:
    input = f.read()

commands = input.split(",")


def string_to_hash(string):
    hash = 0
    for c in string:
        hash = ((hash + ord(c)) * 17) % 256
    return hash

result = 0
for command in commands:
    result += string_to_hash(command)
print(result)