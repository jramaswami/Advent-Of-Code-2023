"""
Advent of Code
Day 20
Pulse Propogation
jramaswami
"""


import collections
import enum


class Pulse(enum.IntEnum):
    Low = 0
    High = enum.auto()


class Status(enum.IntEnum):
    Off = 0
    On = enum.auto()


class Broadcaster:
    def __init__(self, name):
        self.name = name

    def recv(self, pulse, sender):
        return pulse


class FlipFlop:
    def __init__(self, name):
        self.name = name
        self.status = Status.Off

    def recv(self, pulse, sender):
        if pulse == Pulse.Low:
            if self.status == Status.Off:
                self.status = Status.On
                return Pulse.High
            self.status = Status.Off
            return Pulse.Low


class Conjunction:
    def __init__(self, name):
        self.name = name
        self.most_recent_pulse = dict()

    def setup_senders(self, senders):
        # print('Setting up senders for', self.name, senders)
        self.most_recent_pulse = {m: Pulse.Low for m in senders}

    def recv(self, pulse, sender):
        self.most_recent_pulse[sender] = pulse
        # print('\t', self.name, 'recent pulses', self.most_recent_pulse)
        if all(p == Pulse.High for p in self.most_recent_pulse.values()):
            return Pulse.Low
        return Pulse.High


def parse_input(path):
    modules_by_name = dict()
    module_connections = dict()
    reverse_connections = collections.defaultdict(list)
    with open(path, 'r') as infile:
        for line in infile:
            line = line.strip()
            module_token, connections_token = (t.strip() for t in line.split(' -> '))
            connections = [t.strip() for t in connections_token.split(',')]
            module_type, module_name = module_token[0], module_token[1:]
            if module_token == 'broadcaster':
                modules_by_name[module_token] = Broadcaster(module_token)
                module_name = module_token
            elif module_type == '%':
                modules_by_name[module_name] = FlipFlop(module_name)
            elif module_type == '&':
                modules_by_name[module_name] = Conjunction(module_name)
            module_connections[module_name] = connections

            for cx in connections:
                reverse_connections[cx].append(module_name)

    for name, module in modules_by_name.items():
        if isinstance(module, Conjunction):
            module.setup_senders(reverse_connections[name])

    return modules_by_name, module_connections


def push_button(modules_by_name, module_connections):
    low_pulses_sent = high_pulses_sent = 0
    rx_received_low_pulse = False
    queue = collections.deque([('button', 'broadcaster', Pulse.Low)])
    while queue:
        sender, receiver, pulse = queue.popleft()
        # print(sender, pulse, receiver)
        if pulse == Pulse.Low:
            low_pulses_sent += 1
        else:
            high_pulses_sent += 1

        if receiver == 'rx' and pulse == Pulse.Low:
            rx_received_low_pulse = True

        if receiver not in modules_by_name:
            continue

        module = modules_by_name[receiver]
        next_pulse = module.recv(pulse, sender)
        # print('\t', receiver, 'to send', next_pulse)
        if next_pulse is not None:
            for neighbor in module_connections[receiver]:
                queue.append((receiver, neighbor, next_pulse))

    return low_pulses_sent, high_pulses_sent, rx_received_low_pulse


def solve_a(modules_by_name, module_connections):
    low_pulses_sent = high_pulses_sent = 0
    for _ in range(1000):
        lp, hp, _ = push_button(modules_by_name, module_connections)
        low_pulses_sent += lp
        high_pulses_sent += hp
    print(low_pulses_sent, 'low pulses sent', high_pulses_sent, 'high pulses sent')
    soln_a = low_pulses_sent * high_pulses_sent
    return soln_a


def solve_b(modules_by_name, module_connections):
    tick = 0
    while 1:
        tick += 1
        _, _, rx_received_low_pulse = push_button(modules_by_name, module_connections)
        if rx_received_low_pulse:
            return tick
        if tick % 100_000 == 0:
            T = []
            for name in modules_by_name:
                if isinstance(modules_by_name[name], Conjunction):
                    t = modules_by_name[name].most_recent_pulse
                    s = ''.join("1" if v == Pulse.High else "0"  for k, v in t.items())
                    T.append(f'{name} {s}')
            print(tick, ' | '.join(T))
    return -1


def test_solve_a():
    modules_by_name, module_connections = parse_input('../../data/20/test20a.txt')
    assert solve_a(modules_by_name, module_connections) == 32000000
    modules_by_name, module_connections = parse_input('../../data/20/test20b.txt')
    assert solve_a(modules_by_name, module_connections) == 11687500


def main():
    "Main program"
    import pyperclip
    # modules_by_name, module_connections = parse_input('../../data/20/test20a.txt')
    # modules_by_name, module_connections = parse_input('../../data/20/test20b.txt')
    modules_by_name, module_connections = parse_input('../../data/20/input20.txt')
    soln_a = solve_a(modules_by_name, module_connections)
    print('Solution a is', soln_a)
    assert soln_a == 873301506
    soln_b = solve_b(modules_by_name, module_connections)
    print('Solution b is', soln_b)
    pyperclip.copy(soln_b)



if __name__ == '__main__':
    main()