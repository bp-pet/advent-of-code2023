filename = "day4.txt"

with open(filename, "r") as f:
    input = f.read()
lines = input.split("\n")

copies = {k: 1 for k in range(1, len(lines) + 1)}

for line in lines:
    line_index = int(line.split(":")[0].split(" ")[-1])
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
    
    for i in range(line_index + 1, line_index + 1 + winning_count):
        if i > len(lines) + 1:
            break
        copies[i] += copies[line_index]

result = sum(copies[i] for i in copies)

print(result)
