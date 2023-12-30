from itertools import combinations

with open("day12.txt", 'r') as f:
    input = f.read()

lines_raw = input.split("\n")

lines = []
for line_raw in lines_raw:
    conditions, counts_str = line_raw.split(" ")
    counts = [int(i) for i in counts_str.split(",")]
    lines.append((conditions, counts))


def count_missing(line):
    """For a line with ?s, count how many #s still need to be added"""
    total_count = sum(line[1])
    occurences = line[0].count("#")
    return total_count - occurences

def count_questions(line):
    """Count how many question marks are in a line"""
    return line[0].count("?")

def check_validity(line):
    """For a line without ?s, check if it is valid"""
    conditions_lengths = [j for j in [len(i) for i in line[0].split(".")] if j != 0]
    return line[1] == conditions_lengths

def replace_questions(line, selected):
    """
    Replace the question marks of a line with a mask that is the indexed of the selected.
    Returns a new line without the question marks.
    """
    counter = 0
    temp = ""
    for c in line[0]:
        if c == "?":
            temp += "#" if counter in selected else "."
            counter += 1
        else:
            temp += c
    new_line = (temp, line[1])
    return new_line


def generate_variants(n, k):
    return list(combinations(list(range(n)), k))

result = 0
for line in lines:
    variants = generate_variants(count_questions(line), count_missing(line))
    for variant in variants:
        result += 1 if check_validity(replace_questions(line, variant)) else 0

print(result)