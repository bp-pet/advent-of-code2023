filename = "day4.txt"


with open(filename, "r") as f:
    input = f.read()
lines = input.split("\n")

total_score = 0

for line in lines:
    if len(line) == 0:
        continue
    line = line.split(":")[1]
    winning_str = line.split("|")[0]
    winning_list = []
    for s in winning_str.split(" "):
        if len(s) == 0:
            continue
        winning_list.append(int(s))
    mine_str = line.split("|")[1]
    mine_list = []
    for s in mine_str.split(" "):
        if len(s) == 0:
            continue
        mine_list.append(int(s))
    
    winning_count = 0
    for a in mine_list:
        if a in winning_list:
            winning_count += 1
    if winning_count > 0:
        total_score += 2 ** (winning_count - 1)

print(total_score)