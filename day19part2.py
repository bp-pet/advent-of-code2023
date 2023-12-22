with open("day19.txt", 'r') as f:
    input = f.read()

workflows_raw, parts_raw = input.split("\n\n")

class Part:
    def __init__(self, x: int, m: int, a: int, s: int):
        self.x = x
        self.m = m
        self.a = a
        self.s = s
        self.properties = {"x": self.x, "m": self.m, "a": self.a, "s": self.s}
    
    def __str__(self):
        return f"Part with x={self.x}, m={self.m}, a={self.a}, s={self.s}"

class PartRange:
    def __init__(self,
                 x_range: tuple=(1, 4000),
                 m_range: tuple=(1, 4000),
                 a_range: tuple=(1, 4000),
                 s_range: tuple=(1, 4000),
                 current_state: str=("in", 0)):
        self.x = x_range
        self.m = m_range
        self.a = a_range
        self.s = s_range
        self.properties = {"x": self.x, "m": self.m, "a": self.a, "s": self.s}
        self.current_state = current_state
    
    def get_lowest_part(self) -> Part:
        return Part(x=self.x[0], m=self.m[0], a=self.a[0], s=self.s[0])
    
    def get_highest_part(self) -> Part:
        return Part(x=self.x[1], m=self.m[1], a=self.a[1], s=self.s[1])

    def get_new_range(self, parameter, low, high):
        # get new rule with 1 parameter changed
        new_x = self.x
        new_m = self.m
        new_a = self.a
        new_s = self.s
        if parameter == "x":
            new_x = (low, high)
        elif parameter == "m":
            new_m = (low, high)
        elif parameter == "a":
            new_a = (low, high)
        elif parameter == "s":
            new_s = (low, high)
        return PartRange(new_x, new_m, new_a, new_s, current_state=self.current_state)

    def get_value(self):
        return (self.x[1] - self.x[0] + 1) * (self.m[1] - self.m[0] + 1) * (self.a[1] - self.a[0] + 1) * (self.s[1] - self.s[0] + 1)
    
    def __str__(self):
        return f"Part range with x={self.x}, m={self.m}, a={self.a}, s={self.s}, at workflow {self.current_state[0]}, rule {self.current_state[1]}"

class Rule:
    def __init__(self, raw: str):
        if len(raw.split("<")) == 1:
            self.direction = ">"
            self.direction_code = 1
        else:
            self.direction = "<"
            self.direction_code = -1
        self.parameter = raw.split(self.direction)[0]
        self.value = int(raw.split(self.direction)[1].split(":")[0])
        self.outcome = raw.split(":")[1]
    
    def process(self, part):
        if self.direction_code * (part.properties[self.parameter] - self.value) > 0:
            return self.outcome
        else:
            return None
    
    def __str__(self):
        return f"Rule with {self.parameter} {self.direction} {self.value} -> {self.outcome}"


class Workflow:
    def __init__(self, raw: str):
        self.name = raw.split("{")[0]
        rules_raw = raw.split("{")[1][:-1]
        self.rules = [Rule(s) for s in rules_raw.split(",")[:-1]]
        self.final_state = rules_raw.split(",")[-1]
    
    def process(self, part):
        for rule in self.rules:
            outcome = rule.process(part)
            if outcome is not None:
                return outcome
        return self.final_state

    def __str__(self):
        result = f"Workflow \"{self.name}\":"
        for rule in self.rules:
            result += "\n  " + str(rule)
        return result

class PartProcessor:
    def __init__(self, workflows_raw):
        self.workflows = {}
        for w_raw in workflows_raw.split("\n"):
            workflow = Workflow(w_raw)
            self.workflows[workflow.name] = workflow
        self.part_ranges_queue = [PartRange()]
        self.accepted = []
    
    def range_passes_rule(self, part_range, outcome):
        if outcome == "A":
            # add range to accepted, nothing is added to queue
            self.accepted.append(part_range)
        elif outcome == "R":
            # range just disappears
            pass
        else:
            # the state of the range is changed to another workflow and it is added to queue again
            part_range.current_state = (outcome, 0)
            self.part_ranges_queue.append(part_range)
        
    def range_fails_rule(self, part_range):
        part_range.current_state = (part_range.current_state[0], part_range.current_state[1] + 1)
        self.part_ranges_queue.append(part_range)

    def process_all(self):
        while len(self.part_ranges_queue) > 0:
            part_range = self.part_ranges_queue.pop(0)
            workflow = self.workflows[part_range.current_state[0]]
            rule_index = part_range.current_state[1]
            if rule_index == len(workflow.rules):
                # if final state is reached
                outcome = workflow.final_state
                self.range_passes_rule(part_range, outcome)
                continue
            rule = workflow.rules[rule_index]
            low = part_range.get_lowest_part()
            high = part_range.get_highest_part()
            low_result = rule.process(low)
            high_result = rule.process(high)
            if low_result and high_result:
                # whole range passes rule
                outcome = low_result
                self.range_passes_rule(part_range, outcome)
            elif not low_result and not high_result:
                # whole range fails rule
                # range state is updated to next rule in workflow and it is added back to queue
                self.range_fails_rule(part_range)
            else:
                # range is split
                if low_result:
                    passing_range = part_range.get_new_range(rule.parameter, part_range.properties[rule.parameter][0], rule.value - 1)
                    failing_range = part_range.get_new_range(rule.parameter, rule.value, part_range.properties[rule.parameter][1])
                    self.range_passes_rule(passing_range, low_result)
                    self.range_fails_rule(failing_range)
                else:
                    failing_range = part_range.get_new_range(rule.parameter, part_range.properties[rule.parameter][0], rule.value)
                    passing_range = part_range.get_new_range(rule.parameter, rule.value + 1, part_range.properties[rule.parameter][1])
                    self.range_passes_rule(passing_range, high_result)
                    self.range_fails_rule(failing_range)
        
        result = 0
        for pr in self.accepted:
            result += pr.get_value()
        return result

processor = PartProcessor(workflows_raw)
result = processor.process_all()
print(result)