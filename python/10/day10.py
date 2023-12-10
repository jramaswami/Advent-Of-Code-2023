"""
Advent of Code
Day 10
Pipe Maze
jramaswami
"""


import collections


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

    def __eq__(self, other):
        return self.r == other.r and self.c == other.c


NORTH = Posn(-1, 0)
SOUTH = Posn(1, 0)
EAST = Posn(0, 1)
WEST = Posn(0, -1)


def get_neighbors(posn, pipe):
    if pipe == '|':
        return [posn + NORTH, posn + SOUTH]
    if pipe == '-':
        return [posn + EAST, posn + WEST]
    if pipe == 'L':
        return [posn + NORTH, posn + EAST]
    if pipe == 'J':
        return [posn + NORTH, posn + WEST]
    if pipe == '7':
        return [posn + SOUTH, posn + WEST]
    if pipe == 'F':
        return [posn + SOUTH, posn + EAST]
    if pipe == 'S':
        return [posn + p for p in (NORTH, SOUTH, WEST, EAST)]
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
    queue = collections.deque()
    start = find_start(grid)
    dist[start.r][start.c] = 0
    # Determine start neighbors, that is pipes connected to start
    for p in (start + dirn for dirn in (NORTH, SOUTH, EAST, WEST)):
        p_connects_to = get_neighbors(p, grid[p.r][p.c])
        if start in p_connects_to:
            dist[p.r][p.c] = 1
            queue.append(p)
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
    assert soln_a == 6800
    pyperclip.copy(soln_a)


if __name__ == '__main__':
    main()