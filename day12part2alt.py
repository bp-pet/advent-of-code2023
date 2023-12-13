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
        self.line = line
        total_size = len(line[0])
        required = sum(line[1]) + len(line[1]) - 1
        self.num_balls = total_size - required
        self.num_buckets = len(line[1]) + 1

    def check_distribution(self, distribution):
        built = self.generate_output(distribution)
        for i in range(len(built)):
            if self.line[0][i] == "#" and built[i] == ".":
                raise Exception
            elif self.line[0][i] == "." and built[i] == "#":
                return False
        return True
    
    def generate_output(self, distribution):
        built = ""
        for i in range(len(distribution)):
            built += "." * distribution[i]
            if i < len(self.line[1]):
                built += "#" * self.line[1][i] + "."
        built = built[:-1]
        return built

    def distribute_balls(self, distribution):
        if self.check_distribution(distribution):
            num_distributed = sum(distribution)
            if len(distribution) == self.num_buckets:
                return 1 if num_distributed == self.num_balls else 0
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

result = 0
for line in lines[6:7]:
    # print(result)
    result += BallDistributor(line).distribute_balls([])
    print(line)

print(result)