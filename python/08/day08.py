"""
Advent of Code
Day 8
Haunted Wasteland
jramaswami
"""


import collections
import math


Neighbors = collections.namedtuple('Neighbors', ['left', 'right'])


def parse_input(lines):
    # Line one is our instructions
    instructions = lines[0].strip()
    # Skip one line
    graph = {}
    for line in lines[2:]:
        line = line.strip()
        if line:
            u, clause = line.split(' = ')
            neighbors = (t.strip() for t in clause[1:-1].split(','))
            graph[u] = Neighbors(*neighbors)
    return instructions, graph


def solve_a(instructions, graph):
    curr = 'AAA'
    steps = 0
    i = 0
    while curr != 'ZZZ':
        steps += 1
        if instructions[i] == 'L':
            curr = graph[curr].left
        else:
            curr = graph[curr].right
        i += 1
        i %= len(instructions)
    return steps


def test_solve_a_rs():
    with open('../../data/08/test08RL.txt', 'r') as infile:
        lines = infile.readlines()
    instructions, graph = parse_input(lines)
    result = solve_a(instructions, graph)
    assert result == 2


def test_solve_a_llr():
    with open('../../data/08/test08LLR.txt', 'r') as infile:
        lines = infile.readlines()
    instructions, graph = parse_input(lines)
    result = solve_a(instructions, graph)
    assert result == 6


def solve_b(instructions, graph):
    def steps_to_end_with_z(curr):
        steps = 0
        i = 0
        while not curr.endswith('Z'):
            steps += 1
            if instructions[i] == 'L':
                curr = graph[curr].left
            else:
                curr = graph[curr].right
            i += 1
            i %= len(instructions)
        return steps

    # Find all nodes that end in 'A'
    roots = [n for n in graph if n.endswith('A')]
    steps = [steps_to_end_with_z(n) for n in roots]
    soln = math.lcm(*steps)
    return soln


def test_solve_b_():
    with open('../../data/08/test08LR.txt', 'r') as infile:
        lines = infile.readlines()
    instructions, graph = parse_input(lines)
    result = solve_b(instructions, graph)
    assert result == 6


def main():
    "Main program"
    import pyperclip
    import sys
    with open('../../data/08/input08.txt', 'r') as infile:
        lines = infile.readlines()
    instructions, graph = parse_input(lines)
    soln_a = solve_a(instructions, graph)
    print('It takes', soln_a, 'steps to reach ZZZ')
    assert soln_a == 19951
    soln_b = solve_b(instructions, graph)
    print(
        'Starting with all nodes ending in A, it takes',
        soln_b,
        'steps to reach all nodes ending in Z'
    )
    assert soln_b == 16342438708751
    pyperclip.copy(soln_b)


if __name__ == '__main__':
    main()