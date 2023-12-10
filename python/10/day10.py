"""
Advent of Code
Day 10
Pipe Maze
jramaswami
"""


import collections


def read_input(path):
    "Read input from file and return grid"
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
    "Solve first part of the puzzle"
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


def expand_grid(grid):
    "Expand the grid to allow moving between unconnected pipes"
    expanded_grid = []
    for r, row in enumerate(grid):
        expanded_grid.append([])
        for c, val in enumerate(row):
            p = Posn(r, c)
            expanded_grid[-1].append(val)
            expanded_grid[-1].append('.')
        expanded_grid.append(['.' for _ in expanded_grid[-1]])
    return [''.join(row) for row in expanded_grid]


NORTHX = Posn(-2, 0)
SOUTHX = Posn(2, 0)
EASTX = Posn(0, 2)
WESTX = Posn(0, -2)


def get_neighbors_dirn(posn, pipe):
    if pipe == '|':
        return [NORTHX, SOUTHX]
    if pipe == '-':
        return [EASTX, WESTX]
    if pipe == 'L':
        return [NORTHX, EASTX]
    if pipe == 'J':
        return [NORTHX, WESTX]
    if pipe == '7':
        return [SOUTHX, WESTX]
    if pipe == 'F':
        return [SOUTHX, EASTX]
    if pipe == 'S':
        return [NORTHX, SOUTHX, WESTX, EASTX]
    return []


def solve_b(original_grid):
    "Solve second part of the puzzle"
    grid = expand_grid(original_grid)
    dist = [['.' for _ in row] for row in grid]
    visited = [[False for _ in row] for row in grid]
    queue = collections.deque()
    start = find_start(grid)
    dist[start.r][start.c] = 0
    visited[start.r][start.c] = True
    # Determine start neighbors, that is pipes connected to start
    for p in (start + dirn for dirn in (NORTHX, SOUTHX, EASTX, WESTX)):
        for d in get_neighbors_dirn(p, grid[p.r][p.c]):
            p_connects_to = p + d
            if p_connects_to == start:
                dist[p.r][p.c] = 1
                queue.append(p)
                visited[p.r][p.c] = True
    while queue:
        p = queue.popleft()
        for d in get_neighbors_dirn(p, grid[p.r][p.c]):
            p0 = p + d
            if not inbounds(p0, grid):
                continue
            if grid[p0.r][p0.c] == '.':
                continue
            if dist[p0.r][p0.c] == '.':
                dist[p0.r][p0.c] = dist[p.r][p.c] + 1
                visited[p0.r][p0.c] = True
                queue.append(p0)

    # Mark the intermediate steps.
    for r, row in enumerate(visited):
        for c, v in enumerate(row):
            if v:
                p = Posn(r, c)
                for d in get_neighbors_dirn(p, grid[p.r][p.c]):
                    p0 = p + d
                    if not inbounds(p0, grid):
                        continue
                    if visited[p0.r][p0.c]:
                        if d == NORTHX:
                            px = p + NORTH
                        elif d == SOUTHX:
                            px = p + SOUTH
                        elif d == WESTX:
                            px = p + WEST
                        elif d == EASTX:
                            px = p + EAST
                        visited[px.r][px.c] = True

    # Fill from outer edge.
    filled = [[0 for _ in row] for row in visited]
    # Find starting points on outer edge
    queue = collections.deque()
    for c, _ in enumerate(grid[0]):
        if grid[0][c] == '.':
            queue.append(Posn(0, c))
        if grid[0][len(grid)-1] == '.':
            queue.append(Posn(len(grid)-1, c))
    for r, _ in enumerate(grid[1:-1], start=1):
        if grid[r][0] == '.':
            queue.append(Posn(r, 0))
        if grid[r][len(grid[r])-1] == '.':
            queue.append(Posn(r, len(grid[r])-1))

    # Take out any visited spaces
    queue = collections.deque(p for p in queue if not visited[p.r][p.c])

    for p in queue:
        filled[p.r][p.c] = 1
    while queue:
        p = queue.popleft()
        for d in (NORTH, SOUTH, EAST, WEST):
            p0 = p + d
            if p0.r < 0 or p0.c < 0 or p0.r >= len(grid) or p0.c >= len(grid[r]):
                continue
            if visited[p0.r][p0.c]:
                continue
            if not filled[p0.r][p0.c]:
                filled[p0.r][p0.c] = filled[p.r][p.c] + 1
                queue.append(p0)

    for r, row in enumerate(filled):
        for c, v in enumerate(row):
            if visited[r][c]:
                filled[r][c] *= -1

    # Contract grid
    contracted_filled = []
    for r in range(0, len(filled), 2):
        row = []
        for c in range(0, len(filled[r]), 2):
            row.append(filled[r][c] or visited[r][c])
        contracted_filled.append(row)
    soln_a = max(max(0 if x == '.' else x for x in row) for row in dist)
    soln_b = 0
    for r, row in enumerate(contracted_filled):
        for c, f in enumerate(row):
            if not f:
                soln_b += 1
    return soln_a, soln_b


def test_solve_b():
    grid = read_input('../../data/10/test10c.txt')
    _, result = solve_b(grid)
    assert result == 4

    grid = read_input('../../data/10/test10d.txt')
    _, result = solve_b(grid)
    assert result == 8

    grid = read_input('../../data/10/test10e.txt')
    _, result = solve_b(grid)
    assert result == 10


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/10/input10.txt')
    soln_a = solve_a(grid)
    print('The distance to the farthest point is', soln_a)
    assert soln_a == 6800
    soln_a, soln_b = solve_b(grid)
    assert soln_a == 6800
    print('There are', soln_b, 'tiles enclosed in a loop')
    assert soln_b == 483
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()