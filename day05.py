import math

filename = "day5.txt"

class SeedRange:
    def __init__(self, start, size=None, end=None):
        self.start = start
        if size is None:
            self.end = end
            self.size = end - start + 1
        elif end is None:
            self.end = start + size - 1
            self.size = size

    def __str__(self):
        return f"Seed range {self.start}...{self.end}"

class Module:
    def __init__(self, input_str: str):
        self.rules_str = input_str.split("\n")[1:]
        self.create_rules()
        self.fill_gaps()
 
    def create_rules(self):
        self.rules = []
        for rule_str in self.rules_str:
            if rule_str == "":
                continue
            rule_list = [int(i) for i in rule_str.split(" ")]
            self.rules.append(Rule(rule_list[0], rule_list[1], rule_list[2]))
        self.rules = sorted(self.rules, key=lambda x: x.source_start)
    
    def fill_gaps(self):
        current = 0
        new_rules = []
        for rule in self.rules:
            if rule.source_start > current:
                new_rules.append(Rule(current, current, rule.source_start))
            current = rule.source_start + rule.size
        new_rules.append(Rule(self.rules[-1].source_start + self.rules[-1].size, self.rules[-1].source_start + self.rules[-1].size))
        self.rules = self.rules + new_rules
        self.rules = sorted(self.rules, key=lambda x: x.source_start)
    
    def transform_seed_range(self, seed_range: SeedRange):
        result_range = []
        for rule in self.rules:
            if seed_range.end >= rule.source_start and seed_range.end <= rule.source_end:
                # this is the rule
                if seed_range.start >= rule.source_start:
                    # convert whole range using this rule
                    result_range += [SeedRange(start=rule.map_seed(seed_range.start), end=rule.map_seed(seed_range.end))]
                else:
                    # convert top part of range and create new range, continue recursion
                    result_range += [SeedRange(start=rule.map_seed(rule.source_start), end=rule.map_seed(seed_range.end))] + self.transform_seed_range(SeedRange(start=seed_range.start, end=rule.source_start - 1))
        return result_range

    def __str__(self):
        result = "Module:"
        for rule in self.rules:
            result += "\n\t" + str(rule)
        return result

class Rule:
    def __init__(self, target_start: int, source_start: int, size: int=math.inf):
        self.target_start, self.source_start, self.size = target_start, source_start, size
        self.source_end = self.source_start + size - 1
        self.target_end = self.target_start + size - 1

    def map_seed(self, seed: int):
        return (seed - self.source_start) + self.target_start

    def __str__(self):
        return f"Rule {self.source_start}...{self.source_start + self.size - 1} to {self.target_start}...{self.target_start + self.size - 1}"


with open(filename, "r") as f:
    input = f.read()
modules_str = input.split("\n\n")

seeds_ints = [int(i) for i in modules_str[0].split(":")[1].split(" ")[1:]]

seed_ranges = []
for k in range(len(seeds_ints) // 2):
    start = seeds_ints[2 * k]
    size = seeds_ints[2 * k + 1]
    seed_ranges.append(SeedRange(start=start, size=size))

for module_str in modules_str[1:]:
    module = Module(module_str)
    new_seed_ranges = []
    for seed_range in seed_ranges:
        new_seed_ranges += module.transform_seed_range(seed_range)
    seed_ranges = new_seed_ranges

result = min(s.start for s in seed_ranges)
print(result)