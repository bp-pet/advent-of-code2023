with open("day2.txt", "r") as f:
    input = f.read()

# input = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\nGame 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\nGame 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\nGame 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\nGame 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"

lines = input.split("\n")

limits = {"red": 12, "green": 13, "blue": 14}

result = 0

for line in lines:
    if len(line) == 0:
        continue
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