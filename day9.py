with open("day9.txt", 'r') as f:
    input = f.read()

lines = input.split("\n")

def get_next(numbers):
    if numbers == [0] * len(numbers):
        return 0
    diffs = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    return numbers[-1] + get_next(diffs)

def get_prev(numbers):
    if numbers == [0] * len(numbers):
        return 0
    diffs = [numbers[i + 1] - numbers[i] for i in range(len(numbers) - 1)]
    return numbers[0] - get_prev(diffs)

result = 0

for line in lines:
    numbers = [int(i) for i in line.split(" ")]
    result += get_prev(numbers)

print(result)