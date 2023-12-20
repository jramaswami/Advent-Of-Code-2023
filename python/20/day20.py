"""
Advent of Code
Day 20
Pulse Propogation
jramaswami

Part 2 required work outside of just coding.  Inspection of the graph generated
from the module connections (see ../../data/20/graph.svg) shows that rx is fed
by a single conjunction module, &dd.  This module is fed by four other
conjunction modules (&jq, &cc, &nx, &sp) that act as inverters for one
conjunction module each.  This means that when the four modules (&lz, &lk, &ft,
&qr) fire, then rx will receive the pulse in question.

The function solve_b repeats what I did to solve the puzzle mostly by hand.
Observe enough cycles for each of the four conjunction modules of interest to
fire more than once.  We can then compute the cycle length and find the solution
using the LCM.
"""


import collections
import enum
import math


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

    def __str__(self):
        status = 0 if self.status == Status.Off else 1
        return f'%{self.name}={status}'


class Conjunction:
    def __init__(self, name):
        self.name = name
        self.most_recent_pulse = dict()

    def setup_senders(self, senders):
        self.most_recent_pulse = {m: Pulse.Low for m in senders}

    def recv(self, pulse, sender):
        self.most_recent_pulse[sender] = pulse
        if all(p == Pulse.High for p in self.most_recent_pulse.values()):
            return Pulse.Low
        return Pulse.High

    def __str__(self):
        t = ' '.join(f'{k}={0 if v == Pulse.Low else 1}' for k, v in self.most_recent_pulse)
        return f'&{self.name}=({t})'


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
    queue = collections.deque([('button', 'broadcaster', Pulse.Low)])
    while queue:
        sender, receiver, pulse = queue.popleft()
        if pulse == Pulse.Low:
            low_pulses_sent += 1
        else:
            high_pulses_sent += 1

        if receiver not in modules_by_name:
            continue

        module = modules_by_name[receiver]
        next_pulse = module.recv(pulse, sender)
        if next_pulse is not None:
            for neighbor in module_connections[receiver]:
                queue.append((receiver, neighbor, next_pulse))

    return low_pulses_sent, high_pulses_sent


def solve_a(modules_by_name, module_connections):
    low_pulses_sent = high_pulses_sent = 0
    for _ in range(1000):
        lp, hp = push_button(modules_by_name, module_connections)
        low_pulses_sent += lp
        high_pulses_sent += hp
    soln_a = low_pulses_sent * high_pulses_sent
    return soln_a


def test_solve_a():
    modules_by_name, module_connections = parse_input('../../data/20/test20a.txt')
    assert solve_a(modules_by_name, module_connections) == 32000000
    modules_by_name, module_connections = parse_input('../../data/20/test20b.txt')
    assert solve_a(modules_by_name, module_connections) == 11687500


def solve_b(modules_by_name, module_connections):
    # lz, lk, ft, and qr are the key modules
    # When they all fire in the same tick, then rx will receive the pulse
    pulsed = {m: [] for m in ['lz', 'lk', 'ft', 'qr']}
    for tick in range(10000):
        queue = collections.deque([('button', 'broadcaster', Pulse.Low)])
        while queue:
            sender, receiver, pulse = queue.popleft()

            if receiver not in modules_by_name:
                continue

            module = modules_by_name[receiver]
            next_pulse = module.recv(pulse, sender)
            if receiver in ['lz', 'lk', 'ft', 'qr'] and next_pulse == Pulse.Low:
                pulsed[receiver].append(tick)
            if next_pulse is not None:
                for neighbor in module_connections[receiver]:
                    queue.append((receiver, neighbor, next_pulse))

    # Compute the arithmetic's delta for each sequence
    deltas = [pulsed[m][-1] - pulsed[m][-2] for m in pulsed]

    # Compute the LCM of the deltas
    return math.lcm(*deltas)


def main():
    "Main program"
    import pyperclip
    modules_by_name, module_connections = parse_input('../../data/20/input20.txt')
    soln_a = solve_a(modules_by_name, module_connections)
    print('Solution a is', soln_a)
    assert soln_a == 873301506
    soln_b = solve_b(modules_by_name, module_connections)
    print('Solution b is', soln_b)
    assert soln_b == 241823802412393


if __name__ == '__main__':
    main()