"""
Advent of Code
Day 21
Step Counter
jramaswami

REF: https://www.youtube.com/watch?v=9UOMZSL0JTg
Thank you to HyperNeutrino.  There is no way I was going to get the answer!
"""


import collections
import math


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



def fill(start, ticks, grid):
    soln = set()
    visited = set()
    visited.add(start)
    queue = collections.deque()
    queue.append((start, ticks))
    while queue:
        p, d = queue.popleft()
        if d % 2 == 0:
            soln.add(p)
        if d == 0:
            continue
        for p0 in neighbors(p, grid):
            if not inbounds(p0, grid):
                continue
            if grid[p0.row][p0.col] == '#':
                continue
            if p0 in visited:
                continue
            visited.add(p0)
            queue.append((p0, d-1))
    return len(soln)


def test_fill():
    grid = read_input('../../data/21/test21a.txt')
    start = find_start(grid)
    assert fill(start, 6, grid) == 16
    grid = read_input('../../data/21/input21.txt')
    start = find_start(grid)
    assert fill(start, 64, grid) == 3649


def solve_b(grid):
    assert len(grid) == len(grid[0])
    size = len(grid)
    steps = 26501365
    start = find_start(grid)
    assert start.row == start.col == size // 2

    # Number of full grids inside step reach.
    grid_width = steps // size - 1

    odd_grids = (grid_width // 2 * 2 + 1) ** 2
    even_grids = ((grid_width + 1) // 2 * 2) ** 2

    odd_points = fill(start, size * 2 + 1, grid)
    even_points = fill(start, size * 2, grid)

    corner_top = fill(Vector(size-1, start.col), size-1, grid)
    corner_right = fill(Vector(start.row, 0), size-1, grid)
    corner_bottom = fill(Vector(0, start.col), size-1, grid)
    corner_left = fill(Vector(start.row, size-1), size-1, grid)

    small_top_right = fill(Vector(size-1, 0), size // 2 - 1, grid)
    small_top_left = fill(Vector(size-1, size-1), size // 2 - 1, grid)
    small_bottom_right = fill(Vector(0, 0), size // 2 - 1, grid)
    small_bottom_left = fill(Vector(0, size-1), size // 2 - 1, grid)

    large_top_right = fill(Vector(size-1, 0), size * 3 // 2 - 1, grid)
    large_top_left = fill(Vector(size-1, size-1), size * 3 // 2 - 1, grid)
    large_bottom_right = fill(Vector(0, 0), size * 3 // 2 - 1, grid)
    large_bottom_left = fill(Vector(0, size-1), size * 3 // 2 - 1, grid)

    soln_b = (
        (odd_grids * odd_points) + (even_grids * even_points) +
        (corner_top + corner_right + corner_bottom + corner_left) +
        (grid_width + 1) * (small_top_right + small_top_left + small_bottom_right + small_bottom_left) +
        grid_width * (large_top_right + large_top_left + large_bottom_right + large_bottom_left) +
        0
    )
    return soln_b


def main():
    "Main program"
    import pyperclip
    grid = read_input('../../data/21/input21.txt')
    soln_a = solve_a(grid, 64)
    print('The elf can reach', soln_a, 'garden plots in 64 steps')
    assert soln_a == 3649
    pyperclip.copy(str(soln_a))

    soln_b = solve_b(grid)
    print('Solution b', soln_b)
    assert soln_b == 612941134797232
    pyperclip.copy(str(soln_b))


if __name__ == '__main__':
    main()