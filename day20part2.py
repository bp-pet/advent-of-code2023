"""
This solution is based specifically on the given input. Observing it shows that the module
that we are interested in is influenced by 4 other modules. Recording when each of them
becomes active shows that they each have a period. Getting the least common multiple of the
4 periods immediately gives the answer.

It should be noted that there is no guarantee given an arbitrary input that this would even
work. It could even be that the 4 modules in question are periodic for some time, but not
infinitely, which would make this method useless. However, a general solution seems way too
difficult and apparently not needed here.
"""

from math import gcd

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

            # DEBUGGING FOR FINDING MODULE ACTIVATION #####
            if signal.target == "bb":
                if self.modules["bb"].state["xc"] == 1:
                    print(self.current_press)
            ###############################################

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

# required modules are ct, kp, ks, xc
ct_activation = [3796, 7593, 11390]
kp_activation = [3732, 7465, 11198]
ks_activation = [3906, 7813, 11720]
xc_activation = [3822, 7645, 11468]

# make sure the activation of each module is periodic, at least at the start
for l in [ct_activation, kp_activation, ks_activation, xc_activation]:
    assert l[1] - l[0] == l[2] - l[1]

ct_period = ct_activation[1] - ct_activation[0]
kp_period = kp_activation[1] - kp_activation[0]
ks_period = ks_activation[1] - ks_activation[0]
xc_period = xc_activation[1] - xc_activation[0]

periods = [ct_period, kp_period, ks_period, xc_period]

result = 1
for i in periods:
    result = result * i // gcd(result, i)
print(result)