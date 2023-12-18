"""
Advent of Code
Day 18
Lavaduct Legoon
jramaswami

59205 is too high
"""


import collections
import math


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)


DigInstruction = collections.namedtuple('DigInstruction', ['dirn', 'meters', 'color'])


DIRECTIONS = {'R': Vector(0, 1), 'L': Vector(0, -1), 'U': Vector(-1, 0), 'D': Vector(1, 0)}


def read_input(path):
    dig_instructions = []
    with open(path, 'r') as infile:
        for line in infile:
            tokens = line.strip().split()
            dirn = DIRECTIONS[tokens[0].strip()]
            meters = int(tokens[1])
            color = tokens[2][1:-1]
            dig_instructions.append(DigInstruction(dirn, meters, color))
    return dig_instructions


def dig_trench(dig_instructions):
    visited = set()
    posn = Vector(0, 0)
    visited.add(posn)
    for instruction in dig_instructions:
        for _ in range(instruction.meters):
            posn = posn + instruction.dirn
            visited.add(posn)
    return visited


def test_dig_trench():
    dig_instructions = read_input('../../data/18/test18a.txt')
    trench = dig_trench(dig_instructions)
    assert len(trench) == 38


def trench_volume(trench):
    min_cols = collections.defaultdict(lambda: math.inf)
    max_cols = collections.defaultdict(lambda: -math.inf)
    min_row, max_row = math.inf, -math.inf
    for posn in trench:
        min_cols[posn.row] = min(min_cols[posn.row], posn.col)
        max_cols[posn.row] = max(max_cols[posn.row], posn.col)
        min_row = min(min_row, posn.row)
        max_row = max(max_row, posn.row)

    volume = 0
    for row in range(min_row, max_row+1):
        volume += (max_cols[row] - min_cols[row] + 1)
    return volume


def solve_a(dig_instructions):
    trench = dig_trench(dig_instructions)
    soln_a = trench_volume(trench)
    return soln_a


def test_solve_a():
    dig_instructions = read_input('../../data/18/test18a.txt')
    assert solve_a(dig_instructions) == 62


def main():
    "Main program"
    import pyperclip
    dig_instructions = read_input('../../data/18/input18.txt')
    soln_a = solve_a(dig_instructions)
    print('The volume of the trench is', soln_a)
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()