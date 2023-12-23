"""
Advent of Code
Day 23
A Long Walk
jramaswami
"""


import collections


Vector = collections.namedtuple('Vector', ['row', 'col'])
Vector.__add__ = lambda a, b: Vector(a.row + b.row, a.col + b.col)


OFFSETS = (Vector(1, 0), Vector(-1, 0), Vector(0, 1), Vector(0, -1))


def inbounds(p, grid):
    return (
        p.row >= 0 and p.col >= 0 and
        p.row < len(grid) and p.col < len(grid[p.row])
    )


def neighbors(p, grid):
    if grid[p.row][p.col] in 'v^><':
        q = p + OFFSETS['v^><'.index(grid[p.row][p.col])]
        if inbounds(q, grid) and grid[q.row][q.col] != '#':
            yield q
    else:
        for d in OFFSETS:
            q = p + d
            if inbounds(q, grid) and grid[q.row][q.col] != '#':
                yield q


def read_input(path):
    with open(path, 'r') as infile:
        grid = [line.strip() for line in infile]
    return grid


def solve_a(grid):
    start = Vector(0, grid[0].index('.'))
    finish = Vector(len(grid)-1, grid[-1].index('.'))
    visited = set()

    def dfs(p, d):
        visited.add(p)
        if p == finish:
            result = d
        else:
            result = 0
            for q in neighbors(p, grid):
                if q not in visited:
                    result = max(result, dfs(q, d+1))
        visited.remove(p)
        return result

    return dfs(start, 0)


def test_solve_a():
    grid = read_input('../../data/23/test23a.txt')
    assert solve_a(grid) == 94


def main():
    "Main program"
    import pyperclip
    import sys
    sys.setrecursionlimit(pow(10,6))
    grid = read_input('../../data/23/input23.txt')
    soln_a = solve_a(grid)
    print('The longest hike is', soln_a, 'steps')
    assert soln_a == 2074
    pyperclip.copy(str(soln_a))


if __name__ == '__main__':
    main()