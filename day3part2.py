filename = "day3.txt"


with open(filename, "r") as f:
    input = f.read()
lines = input.split("\n")

# preprocess by adding padding
new_lines = []
new_lines.append("." * len(lines[0]))
for line in lines:
    if len(line) == 0:
        continue
    new_lines.append("." + line + ".")
new_lines.append("." * len(lines[0]))
lines = new_lines

symbols = "!@#$%^&*()\|/?,<>~`';\;:][\{\}]-=+_"

def find_numbers(s):
    result = []
    current = ""
    for i, c in enumerate(s):
        if c.isdigit():
            current += c
        elif current != "":
            result.append((int(current), i - len(current)))
            current = ""
    return result

def find_gears(s):
    result = []
    for i, c in enumerate(s):
        if c == "*":
            result += i
    return result


gears = {}
for index, line in enumerate(lines):
    numbers = find_numbers(line)
    for number in numbers:
        for j in range(index - 1, index + 2):
            for i in range(number[1] - 1, number[1] + len(str(number[0])) + 1):
                if lines[j][i] == "*":
                    if (j, i) not in gears:
                        gears[(j, i)] = [number[0]]
                    else:
                        gears[(j, i)].append(number[0])

result = 0
for gear in gears:
    if len(gears[gear]) == 2:
        result += gears[gear][0] * gears[gear][1]
    else:
        print(f"Found gear with {len(gears[gear])} parts")

print(result)