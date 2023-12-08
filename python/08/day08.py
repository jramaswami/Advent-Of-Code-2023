"""
Advent of Code
Day 8
Haunted Wasteland
jramaswami
"""


import collections


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


if __name__ == '__main__':
    main()