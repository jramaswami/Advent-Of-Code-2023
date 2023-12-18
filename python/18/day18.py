"""
Advent of Code
Day 18
Lavaduct Legoon
jramaswami
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


def get_corners(trench):
    "Return the top left and bottom right corners of grid"
    min_row, max_row = math.inf, -math.inf
    min_col, max_col = math.inf, -math.inf
    for posn in trench:
        min_row, max_row = min(min_row, posn.row), max(max_row, posn.row)
        min_col, max_col = min(min_col, posn.col), max(max_col, posn.col)
    return Vector(min_row, min_col), Vector(max_row, max_col)



def print_trench(trench):
    grid = []
    tl, br = get_corners(trench)
    for r in range(tl.row, br.row+1):
        grid_row = []
        for c in range(tl.col, br.col+1):
            if Vector(r,c) in trench:
                grid_row.append('#')
            else:
                grid_row.append('.')
        grid.append(''.join(grid_row))
    print('\n'.join(grid))


def trench_volume(trench):
    # Fill from outside.
    tl, br = get_corners(trench)
    # Move corners outside trench grid
    tl = tl + Vector(-1,-1)
    br = br + Vector(1, 1)
    # Flood fill from outside
    outside = set()
    outside.add(tl)
    queue = collections.deque()
    queue.append(tl)
    while queue:
        curr = queue.popleft()
        for dirn in DIRECTIONS.values():
            neighbor = curr + dirn
            if (tl.row <= neighbor.row <= br.row) and (tl.col <= neighbor.col <= br.col):
                if neighbor in trench:
                    continue
                if neighbor not in outside:
                    outside.add(neighbor)
                    queue.append(neighbor)
    volume = (br.row - tl.row + 1) * (br.col - tl.col + 1)
    volume -= len(outside)
    return volume


def solve_a(dig_instructions):
    trench = dig_trench(dig_instructions)
    soln_a = trench_volume(trench)
    return soln_a


def test_solve_a():
    dig_instructions = read_input('../../data/18/test18a.txt')
    assert solve_a(dig_instructions) == 62


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


def solve_b(dig_instructions):
    dig_instructions0 = translate_dig_instructions(dig_instructions)
    soln_b = solve_a(dig_instructions0)
    return soln_b


def test_solve_b():
    dig_instructions = read_input('../../data/18/test18a.txt')
    assert solve_b(dig_instructions) == 952408144115


def main():
    "Main program"
    import pyperclip
    # dig_instructions = read_input('../../data/18/test18a.txt')
    dig_instructions = read_input('../../data/18/input18.txt')
    soln_a = solve_a(dig_instructions)
    print('The volume of the trench is', soln_a)
    assert soln_a == 39194
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()