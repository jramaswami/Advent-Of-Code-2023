"""
Advent of Code
Day 21
Step Counter
jramaswami
"""


import collections


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)


OFFSETS = (Vector(1,0), Vector(-1,0), Vector(0,1), Vector(0,-1))


def read_input(path):
    with open(path, 'r') as infile:
        grid = [line.strip() for line in infile]
    return grid


def inbounds(p, grid):
    return p.row >= 0 and p.col >=0 and p.row < len(grid) and p.col < len(grid[p.row])


def neighbors(p, grid):
    for off in OFFSETS:
        p0 = p + off
        if inbounds(p0, grid):
            yield p0


def find_start(grid):
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if grid[r][c] == 'S':
                return Vector(r, c)


def solve_a(grid, ticks):
    curr_queue = set()
    curr_queue.add(find_start(grid))
    next_queue = set()
    for _ in range(ticks):
        for p in curr_queue:
            for p0 in neighbors(p, grid):
                if grid[p0.row][p0.col] != '#':
                    next_queue.add(p0)
        curr_queue, next_queue = next_queue, set()
    return len(curr_queue)


def test_solve_a():
    grid = read_input('../../data/21/test21a.txt')
    assert solve_a(grid, 6) == 16


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/21/input21.txt')
    soln_a = solve_a(grid, 64)
    print('The elf can reach', soln_a, 'garden plots in 64 steps')
    assert soln_a == 3649
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()