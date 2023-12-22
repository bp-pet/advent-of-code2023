with open("day19.txt", 'r') as f:
    input = f.read()

workflows_raw, parts_raw = input.split("\n\n")

class Part:
    def __init__(self, raw: str):
        split_str = raw.split(",")
        self.x = int(split_str[0][3:])
        self.m = int(split_str[1][2:])
        self.a = int(split_str[2][2:])
        self.s = int(split_str[3][2:-1])
        self.properties = {"x": self.x, "m": self.m, "a": self.a, "s": self.s}
    
    def __str__(self):
        return f"Part with x={self.x}, m={self.m}, a={self.a}, s={self.s}"

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
    def __init__(self, parts_raw, workflows_raw):
        self.parts = [Part(p) for p in parts_raw.split("\n")]
        self.workflows = {}
        for w_raw in workflows_raw.split("\n"):
            workflow = Workflow(w_raw)
            self.workflows[workflow.name] = workflow

    def process_all(self):
        accepted = []
        for part in self.parts:
            current = "in"
            while True:
                workflow = self.workflows[current]
                current = workflow.process(part)
                if current == "A":
                    accepted.append(part)
                    break
                elif current == "R":
                    break
        result = 0
        for part in accepted:
            result += sum(part.properties[k] for k in part.properties)
        return result

print(PartProcessor(parts_raw, workflows_raw).process_all())