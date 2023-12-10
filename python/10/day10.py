"""
Advent of Code
Day 10
Pipe Maze
jramaswami

6784 is too low
"""


import collections
import math


def read_input(path):
    with open(path,'r') as infile:
        grid = [line.strip() for line in infile.readlines()]
    return grid


class Posn:
    def __init__(self, r, c):
        self.r = r
        self.c = c

    def __add__(self, other):
        return Posn(self.r + other.r, self.c + other.c)

    def __hash__(self):
        return hash((self.r, self.c))

    def __repr__(self):
        return f'Posn({self.r}, {self.c})'


UP = Posn(-1, 0)
DOWN = Posn(1, 0)
RIGHT = Posn(0, 1)
LEFT = Posn(0, -1)


def get_neighbors(posn, pipe):
    if pipe == '|':
        return [posn + UP, posn + DOWN]
    if pipe == '-':
        return [posn + LEFT, posn + RIGHT]
    if pipe == 'L':
        return [posn + UP, posn + RIGHT]
    if pipe == 'J':
        return [posn + UP, posn + LEFT]
    if pipe == '7':
        return [posn + LEFT, posn + DOWN]
    if pipe == 'F':
        return [posn + DOWN, posn + RIGHT]
    if pipe == 'S':
        return [posn + p for p in (UP, DOWN, LEFT, RIGHT)]
    return []


def inbounds(posn, lines):
        r, c = posn.r, posn.c
        return r >= 0 and c >= 0 and r < len(lines) and c < len(lines[r])


def find_start(lines):
    for r, row in enumerate(lines):
        for c, val in enumerate(row):
            if val == 'S':
                return Posn(r, c)


def solve_a(grid):
    dist = [['.' for _ in row] for row in grid]
    start = find_start(grid)
    dist[start.r][start.c] = 0
    queue = collections.deque([start])
    while queue:
        p = queue.popleft()
        for p0 in get_neighbors(p, grid[p.r][p.c]):
            if not inbounds(p0, grid):
                continue
            if grid[p0.r][p0.c] == '.':
                continue
            if dist[p0.r][p0.c] == '.':
                dist[p0.r][p0.c] = dist[p.r][p.c] + 1
                queue.append(p0)

    return max(max(0 if x == '.' else x for x in row) for row in dist)


def test_solve_a():
    grid = read_input('../../data/10/test10a.txt')
    assert solve_a(grid) == 4
    grid = read_input('../../data/10/test10b.txt')
    assert solve_a(grid) == 8


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/10/input10.txt')
    soln_a = solve_a(grid)
    print('The distance to the farthest point is', soln_a)
    pyperclip.copy(soln_a)


if __name__ == '__main__':
    main()