class Signal:
    def __init__(self, pulse: int, source: str, target: str):
        self.pulse = pulse
        self.source = source
        self.target = target
    
    def __str__(self):
        return f"Signal with pulse {self.pulse} from {self.source} to {self.target}"

class Module:
    def __init__(self, name: str, targets: str):
        raise NotImplementedError()
    
    def handle_signal(self, signal: Signal) -> list[Signal]:
        raise NotImplementedError()
    
    def create_signals_to_all_targets(self, pulse: int):
        return [Signal(pulse, self.name, target) for target in self.targets]
    
    def __str__(self):
        return f"{self.symbol}{self.name} -> {self.targets}; state {self.state}"

class FlipFlop(Module):
    def __init__(self, name: str, targets: list[str]):
        self.name = name
        self.targets = targets
        self.state = 0
        self.symbol = "%"
    
    def handle_signal(self, signal: Signal) -> list[Signal]:
        if signal.pulse:
            return []
        else:
            self.state = 1 - self.state
            return self.create_signals_to_all_targets(self.state)
    
    def __str__(self):
        return f"{self.symbol}{self.name} -> {self.targets}; state {self.state}"

class Conjunction(Module):
    def __init__(self, name: str, targets: list[str]):
        self.name = name
        self.targets = targets
        self.state = {}
        self.symbol = "&"
    
    def add_source(self, source: str):
        self.state[source] = 0

    def handle_signal(self, signal: Signal):
        if self.state is None:
            raise Exception("Need to set sources for conjunction first")
        self.state[signal.source] = signal.pulse
        if all(v == 1 for v in self.state.values()):
            return self.create_signals_to_all_targets(0)
        else:
            return self.create_signals_to_all_targets(1)

class Broadcaster(Module):
    def __init__(self, name: str, targets: list[str]):
        self.name = name
        self.targets = targets
        self.state = "-"
        self.symbol = ""
    
    def handle_signal(self, signal: Signal):
        return self.create_signals_to_all_targets(signal.pulse)

class SignalProcessor:
    def __init__(self, modules: list[Module]):
        self.modules = {module.name: module for module in modules}
        self.signals = None
        self.get_inputs_for_conjunctions()
        self.output_log = {0: 0, 1: 0}
        self.current_press = None
    
    def get_inputs_for_conjunctions(self):
        for module_name in self.modules:
            module = self.modules[module_name]
            targets = module.targets
            for target in targets:
                if target not in self.modules:
                    continue
                if isinstance(self.modules[target], Conjunction):
                    self.modules[target].add_source(module_name)
    
    def process_button_press(self):
        self.signals = [Signal(0, None, "broadcaster")]
        while len(self.signals) > 0:
            signal = self.signals.pop(0)
            self.output_log[signal.pulse] += 1
            if signal.target == "bb":
                if self.modules["bb"].state["xc"] == 1:
                    print(self.current_press)
            if signal.target not in self.modules:
                continue
            target = self.modules[signal.target]
            self.signals += target.handle_signal(signal)
    
    def process_n_presses(self, n: int):
        for self.current_press in range(n):
            self.process_button_press()
    
    def get_result(self):
        return self.output_log[0] * self.output_log[1]

    def __str__(self):
        result = ""
        for module_str in self.modules:
            result += str(self.modules[module_str]) + "\n"
        return result[:-1]
    
class Parser:
    def __init__(self, filename: str):
        self.filename = filename
    
    def parse(self) -> SignalProcessor:
        with open(self.filename, 'r') as f:
            raw = f.read()
        modules = []
        for line in raw.split("\n"):
            temp = line.split(" ")
            name = temp[0][1:]
            targets = [i[:-1] for i in temp[2:-1]] + [temp[-1]]
            if line[0] == "%":
                modules.append(FlipFlop(name, targets))
            elif line[0] == "&":
                modules.append(Conjunction(name, targets))
            elif line[0] == "b":
                modules.append(Broadcaster("broadcaster", targets))
            else:
                raise Exception("Invalid module")
        return SignalProcessor(modules)

processor = Parser("day20.txt").parse()
# processor.process_n_presses(100000)


ct = [3796, 7593, 11390]
kp = [3732, 7465, 11198]
ks = [3906, 7813, 11720]
xc = [3822, 7645, 11468]

for l in [ct, kp, ks, xc]:
    assert l[1] - l[0] == l[2] - l[1]

ct_diff = ct[1] - ct[0]
kp_diff = kp[1] - kp[0]
ks_diff = ks[1] - ks[0]
xc_diff = xc[1] - xc[0]

diffs = [ct_diff, kp_diff, ks_diff, xc_diff]


from math import gcd
lcm = 1
for i in diffs:
    lcm = lcm*i//gcd(lcm, i)
print(lcm)