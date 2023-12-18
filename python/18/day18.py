"""
Advent of Code
Day 18
Lavaduct Legoon
jramaswami

Got a hint about how to adjust the following formula:

A = 1/2 * SUM[p_x - q_x) * (p_y + q_y)] for p,q in edges

REF: https://cp-algorithms.com/geometry/area-of-simple-polygon.html
REF: https://www.reddit.com/r/adventofcode/comments/18lj7wx/2023_day_18_how_do_you_adapt_the_shoelace_formula/
"""


import collections
import math


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)
Vector.__mul__ = lambda a, b: Vector(a.row * b, a.col * b)


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


def decode_color(color):
    meters = int(color[1:6], base=16)
    dirn = 'RDLU'[int(color[-1])]
    return dirn, meters


def test_decode_color():
    colors, expected = [], []
    with open('../../data/18/test18b.txt', 'r') as infile:
        for line in infile:
            line = line.strip()
            color, tokens = (t.strip() for t in line.split('='))
            dirn, meters = tokens.split()
            meters = int(meters)
            colors.append(color)
            expected.append((dirn, meters))

    for color, exp in zip(colors, expected):
        assert decode_color(color) == exp


def translate_dig_instructions(dig_instructions):
    dig_insructions0 = []
    for dig in dig_instructions:
        dirn, meters = decode_color(dig.color)
        dig_insructions0.append(DigInstruction(DIRECTIONS[dirn], meters, dig.color))
    return dig_insructions0


def solve(dig_instructions):
    volume = 0
    curr_posn = Vector(0, 0)
    perimeter = 0
    adjustment = 1
    for i, instruction in enumerate(dig_instructions):
        next_posn = curr_posn + (instruction.dirn * instruction.meters)
        if instruction.dirn.row < 0 or instruction.dirn.col < 0:
            adjustment += instruction.meters
        volume += (curr_posn.col - next_posn.col) * (curr_posn.row + next_posn.row)
        perimeter += instruction.meters
        curr_posn = next_posn
    return (volume // 2) + adjustment


def test_solve_b():
    dig_instructions = read_input('../../data/18/test18a.txt')
    assert solve(dig_instructions) == 62
    assert solve(translate_dig_instructions(dig_instructions)) == 952408144115
    dig_instructions = read_input('../../data/18/input18.txt')
    assert solve(dig_instructions) == 39194


def main():
    "Main program"
    import pyperclip
    dig_instructions = read_input('../../data/18/input18.txt')
    soln_a = solve(dig_instructions)
    print('The volume of the trench is', soln_a)
    assert soln_a == 39194
    pyperclip.copy(str(soln_a))
    soln_b = solve(translate_dig_instructions(dig_instructions))
    print('The volume of the hexadecimal lagoon is', soln_b)
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()