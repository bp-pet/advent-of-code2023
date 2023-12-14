with open("day12.txt", 'r') as f:
    input = f.read()

lines_raw = input.split("\n")

lines = []
for line_raw in lines_raw:
    conditions_str, counts_str = line_raw.split(" ")
    conditions = conditions_str
    counts = [int(i) for i in counts_str.split(",")]
    lines.append((conditions, counts))

# make into 5
# new_lines = []
# for line in lines:
#     temp = list(line[0])
#     new_conds = "".join((temp + ["?"]) * 5)[:-1]
#     new_counts = line[1] * 5
#     new_lines.append((new_conds, new_counts))
# lines = new_lines

def check_validity_of_partial(line):
    """
    For a partially filled line, check if it is feasible up to the question marks.
    """
    num_questions = line[0].count("?")
    num_hashtags = line[0].count("#")
    num_required = sum(line[1])
    if num_questions == 0:
        return check_validity_of_complete(line)
    if num_hashtags > num_required or num_required - num_hashtags > num_questions:
        return 0
    conds_str = str(line[0])
    built = conds_str.split("?")[0]
    conditions_lengths = [j for j in [len(i) for i in built.split(".")] if j != 0]
    if len(conditions_lengths) > len(line[1]):
        return 0
    for i, c in enumerate(conditions_lengths):
        if i == len(conditions_lengths) - 1:
            if c > line[1][i]:
                return 0
        else:
            if c != line[1][i]:
                return 0
    return 1

def check_validity_of_complete(line):
    """
    For a line without ?s, check if it is valid.
    """
    conditions_lengths = [j for j in [len(i) for i in line[0].split(".")] if j != 0]
    on_one = False
    for i in range(len(line[0])):
        c = line[0][i]
        if c == "#":
            pass
    return line[1] == conditions_lengths

def find_next_sequence(string, search_start):
    for i in range(search_start, len(string)):
        if string[i] == "#":
            found_start = i
            break
    for i in range(found_start + 1, len(string)):
        if string[i] == "#":
            found_end = i
            break
    return (found_start, found_end)

def try_branches(line):
    if line[0].count("?") == 0:
        return check_validity_of_complete(line)
    first = line[0].find("?")
    score = 0
    for c in [".", "#"]:
        temp = list(line[0])
        temp[first] = c
        alt_line = ("".join(temp), line[1])
        if check_validity_of_partial(alt_line):
            score += try_branches(alt_line)
    return score

results = ""
summ = 0
for line in lines:
    # print(line)
    # go through the question marks from left to right, branch on each one being
    # yes/no, then cut a lot of branches because they are not feasible
    results += str(try_branches(line)) + "\n"
    summ += try_branches(line)

with open("test2.txt", 'w') as f:
    f.write(results)

print(summ)