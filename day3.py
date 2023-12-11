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

result = 0

for index, line in enumerate(lines):
    numbers = find_numbers(line)
    for number in numbers:
        flag = False
        for j in range(index - 1, index + 2):
            for i in range(number[1] - 1, number[1] + len(str(number[0])) + 1):
                if lines[j][i] in symbols:
                    flag = True
                    break
        if flag:
            result += number[0]

print(result)