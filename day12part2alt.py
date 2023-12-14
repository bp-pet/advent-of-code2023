with open("day12demo.txt", 'r') as f:
    input = f.read()

lines_raw = input.split("\n")

lines = []
for line_raw in lines_raw:
    conditions_str, counts_str = line_raw.split(" ")
    conditions = conditions_str
    counts = [int(i) for i in counts_str.split(",")]
    lines.append((conditions, counts))

# make into 5
new_lines = []
for line in lines:
    temp = list(line[0])
    new_conds = "".join((temp + ["?"]) * 5)[:-1]
    new_counts = line[1] * 5
    new_lines.append((new_conds, new_counts))
lines = new_lines

class BallDistributor:
    def __init__(self, line):
        self.string = line[0]
        self.sequence = line[1]
        self.line_string_size = len(self.string)
        self.line_sequence_size = len(self.sequence)
        required = sum(self.sequence) + self.line_sequence_size - 1
        self.num_balls = self.line_string_size - required
        self.num_buckets = self.line_sequence_size + 1

    def check_distribution(self, distribution):
        # FIXES: DON'T GENERATE WHOLE STRING, JUST CHECK IF LAST ADDITION TO DIST WORKS
        # previous ones are already checked
        old_size = len(distribution) - 1
        if old_size == -1:
            return True
        start_gap = sum(self.sequence[:old_size]) + old_size + sum(distribution[:old_size])
        start_seq = start_gap + distribution[-1]
        last_bit = start_seq + self.sequence[old_size]
        for i in range(start_gap, start_seq):
            if self.string[i] == "#":
                raise Exception
        for i in range(start_seq, last_bit):
            if self.string[i] == ".":
                return False
        if last_bit < self.line_string_size and self.string[last_bit] == "#":
            return False
        if len(distribution) == self.line_sequence_size:
            for i in range(last_bit, self.line_string_size):
                if self.string[i] == ".":
                    return False
        return True

    def distribute_balls(self, distribution):
        if self.check_distribution(distribution):
            num_distributed = sum(distribution)
            if len(distribution) == len(self.sequence):
                return 1
            left_to_distribute = self.num_balls - num_distributed
            result = 0
            for i in range(left_to_distribute + 1):
                try:
                    result += self.distribute_balls(distribution + [i])
                except:
                    break
            return result
        else:
            return 0

class Distribution:
    def __init__(self, dist_list):
        self.dist_list = dist_list
        self.number_of_elements = len(dist_list)
        self.size = sum(dist_list)

result = 0
for line in lines:
    result = BallDistributor(line).distribute_balls([])
    print(result)

# print(result)

# ball = BallDistributor(lines[0])
# print(ball.line)
# # result = ball.check_distribution([0] * 15)
# result = ball.distribute_balls([])
# print(result)