with open("day1.txt", "r") as f:
    input = f.read()

lines = input.split("\n")

result = 0
for line in lines:
    digits = []
    for c in line:
        if c.isdigit():
            digits.append(c)
    this_digit = int(digits[0] + digits[-1])
    result += this_digit

print(result)