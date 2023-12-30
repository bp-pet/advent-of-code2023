import numpy as np

with open("day12.txt", 'r') as f:
    input = f.read()

lines_raw = input.split("\n")

lines = []
for line_raw in lines_raw:
    conditions_str, counts_str = line_raw.split(" ")
    conditions = conditions_str
    counts = [int(i) for i in counts_str.split(",")]
    lines.append((conditions, counts))

# multiply input by 5
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
        self.spaces_to_distribute = self.line_string_size - required

        self.lookup_array = None

    def is_feasible(self, distribution, next):
        start_gap = sum(self.sequence[:distribution.size]) + distribution.size + distribution.summ
        start_seq = start_gap + next
        last_bit = start_seq + self.sequence[distribution.size]
        for i in range(start_gap, start_seq):
            if self.string[i] == "#":
                return False
        for i in range(start_seq, last_bit):
            if self.string[i] == ".":
                return False
        if last_bit < self.line_string_size and self.string[last_bit] == "#":
            return False
        if distribution.size == self.line_sequence_size:
            for i in range(last_bit, self.line_string_size):
                if self.string[i] == ".":
                    return False
        return True

    def main(self):
        if self.spaces_to_distribute == 0:
            return 1
        self.lookup_array = - np.ones([self.line_sequence_size, self.spaces_to_distribute + 1])
        return int(self.loop(Distribution(0, 0)))
    
    def check_last_bits(self, distribution):
        sequence_end = distribution.summ + distribution.size + sum(self.sequence)
        for i in range(sequence_end, self.line_string_size):
            if self.string[i] == "#":
                return False
        return True
    
    def loop(self, distribution):
        if distribution.size == self.line_sequence_size:
            return self.check_last_bits(distribution)
        if self.lookup_array[distribution.size, distribution.summ] != -1:
            return self.lookup_array[distribution.size, distribution.summ]
        balls_left_to_distribute = self.spaces_to_distribute - distribution.summ
        result = 0
        for i in range(balls_left_to_distribute + 1):
            if self.is_feasible(distribution, i):
                result += self.loop(distribution.increment(i))
        self.lookup_array[distribution.size, distribution.summ] = result
        return result

class Distribution:
    def __init__(self, size, summ):
        self.size = size
        self.summ = summ
    
    def increment(self, amount):
        return Distribution(self.size + 1, self.summ + amount)

result = 0
for line in lines:
    result += BallDistributor(line).main()
print(result)