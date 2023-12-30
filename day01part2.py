with open("day1.txt", "r") as f:
    input = f.read()


numbers = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9}
numbers3 = ["one", "two", "six"]
numbers4 = ["four", "five", "nine"]
numbers5 = ["three", "seven", "eight"]

lines = input.split("\n")

result = 0
for line in lines:

    # scan forward until digit is found
    for i, c in enumerate(line):
        if c.isdigit():
            first_digit = c
            break
        elif line[i:i+3] in numbers3:
            first_digit = str(numbers[line[i:i+3]])
            break
        elif line[i:i+4] in numbers4:
            first_digit = str(numbers[line[i:i+4]])
            break
        elif line[i:i+5] in numbers5:
            first_digit = str(numbers[line[i:i+5]])
            break

    # scan backward until digit is found
    for i, c in enumerate(line[::-1]):
        if c.isdigit():
            second_digit = c
            break
        a3 = line[::-1][i:i+3][::-1]
        a4 = line[::-1][i:i+4][::-1]
        a5 = line[::-1][i:i+5][::-1]
        if a3 in numbers3:
            second_digit = str(numbers[a3])
            break
        if a4 in numbers4:
            second_digit = str(numbers[a4])
            break
        if a5 in numbers5:
            second_digit = str(numbers[a5])
            break
    this_digit = int(first_digit + second_digit)
    result += this_digit

print(result)