with open("day2.txt", "r") as f:
    input = f.read()

lines = input.split("\n")

limits = {"red": 12, "green": 13, "blue": 14}

result = 0

for line in lines:
    id = int(line.split(":")[0].split(" ")[1])
    groups = line.split(":")[1].split(";")
    good = True
    for group in groups:
        piles = group[1:].split(", ")
        for pile in piles:
            number = int(pile.split(" ")[0])
            color = pile.split(" ")[1]
            if number > limits[color]:
                good = False
    if good:
        result += id

print(result)