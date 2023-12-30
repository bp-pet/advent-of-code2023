with open("day2.txt", "r") as f:
    input = f.read()

lines = input.split("\n")

result = 0

for line in lines:
    if len(line) == 0:
        continue
    current = {"red": 0, "blue": 0, "green": 0}
    id = int(line.split(":")[0].split(" ")[1])
    groups = line.split(":")[1].split(";")
    for group in groups:
        piles = group[1:].split(", ")
        for pile in piles:
            number = int(pile.split(" ")[0])
            color = pile.split(" ")[1]
            if number > current[color]:
                current[color] = number
    power = 1
    for k in current:
        power = power * current[k]
    result += power


print(result)